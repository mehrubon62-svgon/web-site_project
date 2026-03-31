import json
import os
import re
from urllib import error, request as urllib_request

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST

from ai_consultant.models import ChatMessage, ChatSession
from my_site_app.models import Case, GPU, Laptop, Motherboard, PowerSupply, Processor, RAM, Storage

OPENROUTER_MODEL = "openrouter/auto"


def _get_or_create_chat_session(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    if request.user.is_authenticated:
        chat_session, _ = ChatSession.objects.get_or_create(
            session_id=session_key,
            defaults={"user": request.user},
        )
        if chat_session.user_id != request.user.id:
            chat_session.user = request.user
            chat_session.save(update_fields=["user", "updated_at"])
        return chat_session

    chat_session, _ = ChatSession.objects.get_or_create(session_id=session_key)
    return chat_session


def _get_or_create_product_chat_session(request, product_model, product_id):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    scoped_session_id = f"{session_key}:product:{product_model}:{product_id}"

    defaults = {}
    if request.user.is_authenticated:
        defaults["user"] = request.user

    chat_session, _ = ChatSession.objects.get_or_create(
        session_id=scoped_session_id,
        defaults=defaults,
    )
    if request.user.is_authenticated and chat_session.user_id != request.user.id:
        chat_session.user = request.user
        chat_session.save(update_fields=["user", "updated_at"])
    return chat_session


def _build_catalog_snapshot():
    top_cpus = list(Processor.objects.filter(stock__gt=0).order_by("price")[:8])
    top_gpus = list(GPU.objects.filter(stock__gt=0).order_by("price")[:8])
    top_laptops = list(Laptop.objects.filter(stock__gt=0).order_by("price")[:8])

    return {
        "processors": [
            {
                "name": item.name,
                "manufacturer": item.manufacturer,
                "socket": item.socket,
                "cores": item.cores,
                "threads": item.threads,
                "price": float(item.price),
                "stock": item.stock,
            }
            for item in top_cpus
        ],
        "gpus": [
            {
                "name": item.name,
                "manufacturer": item.manufacturer,
                "chipset": item.chipset,
                "vram": item.vram,
                "recommended_psu": item.recommended_psu,
                "price": float(item.price),
                "stock": item.stock,
            }
            for item in top_gpus
        ],
        "laptops": [
            {
                "name": item.name,
                "manufacturer": item.manufacturer,
                "category": item.category,
                "ram_size": item.ram_size,
                "storage_size": item.storage_size,
                "price": float(item.price),
                "stock": item.stock,
            }
            for item in top_laptops
        ],
    }


def _get_openrouter_key():
    return os.getenv("OPENROUTER_API_KEY")


def _normalize_assistant_text(text):
    cleaned = (text or "").strip()
    cleaned = cleaned.replace("**", "")
    cleaned = cleaned.replace("__", "")
    cleaned = cleaned.replace("```", "")
    return cleaned


def _detect_user_language(text):
    value = text or ""
    has_cyrillic = bool(re.search(r"[А-Яа-яЁё]", value))
    if has_cyrillic:
        return "ru"
    return "en"


def _is_response_in_language(text, lang):
    value = text or ""
    cyr = len(re.findall(r"[А-Яа-яЁё]", value))
    lat = len(re.findall(r"[A-Za-z]", value))
    if lang == "ru":
        return cyr >= max(6, lat // 2)
    return lat >= max(6, cyr // 2)


def _force_single_language(text, lang):
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    kept = []
    for line in lines:
        cyr = len(re.findall(r"[А-Яа-яЁё]", line))
        lat = len(re.findall(r"[A-Za-z]", line))
        if lang == "ru":
            if cyr == 0 and lat > 0:
                continue
        else:
            if lat == 0 and cyr > 0:
                continue
        kept.append(line)

    if kept:
        return "\n".join(kept)
    return text


def _rewrite_to_language(text, target_lang, api_key):
    if not text.strip():
        return text
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    f"Rewrite the text strictly in {target_lang} language only. "
                    "Keep meaning same. Plain text only. Do not add extra info."
                ),
            },
            {"role": "user", "content": text},
        ],
        "temperature": 0.0,
        "max_tokens": 420,
    }
    req = urllib_request.Request(
        url="https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "BuildBox Language Guard",
        },
        method="POST",
    )
    try:
        with urllib_request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            choices = data.get("choices") or []
            if choices:
                content = choices[0].get("message", {}).get("content", "")
                if isinstance(content, str) and content.strip():
                    return _force_single_language(_normalize_assistant_text(content), target_lang)
    except Exception:
        pass
    return text


def _extract_memory_facts(user_text):
    text = (user_text or "").lower()
    facts = []

    budget_match = re.search(r"(\$?\s?\d{3,6})", user_text or "")
    if budget_match:
        facts.append(f"Budget mentioned: {budget_match.group(1).strip()}")

    if any(k in text for k in ["gaming", "game", "игр", "fps"]):
        facts.append("Primary goal: gaming")
    if any(k in text for k in ["work", "office", "работ", "офис"]):
        facts.append("Primary goal: work/office")
    if any(k in text for k in ["editing", "video", "монтаж", "рендер"]):
        facts.append("Primary goal: content creation")
    if any(k in text for k in ["quiet", "silent", "тих", "noise"]):
        facts.append("Preference: quiet build")
    if any(k in text for k in ["intel", "amd", "nvidia", "asus", "msi"]):
        facts.append("Brand preference mentioned")

    return facts


def _update_chat_memory(chat_session, user_text):
    facts = _extract_memory_facts(user_text)
    if not facts:
        return ""

    memory_msg = (
        chat_session.messages.filter(role="SYSTEM", content__startswith="MEMORY:")
        .order_by("-created_at")
        .first()
    )
    existing = ""
    if memory_msg:
        existing = memory_msg.content.replace("MEMORY:", "", 1).strip()

    current_facts = set([line.strip() for line in existing.split("\n") if line.strip()])
    for fact in facts:
        current_facts.add(fact)

    merged = "\n".join(sorted(current_facts))
    ChatMessage.objects.create(
        session=chat_session,
        role="SYSTEM",
        content=f"MEMORY:\n{merged}",
    )
    return merged


def _generate_ai_reply(user_text, chat_session):
    api_key = _get_openrouter_key()
    if not api_key:
        return (
            "AI is not configured yet. Add OPENROUTER_API_KEY in your environment, "
            "then BuildBox AI will answer with real AI recommendations."
        )

    catalog = _build_catalog_snapshot()
    recent_messages = list(chat_session.messages.order_by("-created_at")[:12])[::-1]
    conversation = [
        {"role": message.role.lower(), "content": message.content}
        for message in recent_messages
        if message.role in {"USER", "ASSISTANT"}
    ]
    memory_summary = (
        chat_session.messages.filter(role="SYSTEM", content__startswith="MEMORY:")
        .order_by("-created_at")
        .values_list("content", flat=True)
        .first()
    ) or "No long-term memory yet."

    system_prompt = (
        "You are BuildBox AI, an AI consultant for computers and PC building only.\n"
        "Identity rules:\n"
        "- Your name is BuildBox AI.\n"
        "- Never say you have another name.\n"
        "Domain rules:\n"
        "- You must answer ONLY computer-related topics: PCs, laptops, components, compatibility, performance, cooling, PSU, peripherals, operating systems, and troubleshooting.\n"
        "- If user asks about non-computer topics, refuse briefly and steer back to computer topics.\n"
        "- Do not provide politics, medical, legal, relationship, or other off-topic advice.\n"
        "Catalog rules:\n"
        "- Prefer recommendations from provided catalog data.\n"
        "- Never invent products that are not in the provided catalog.\n"
        "- Mention compatibility constraints where relevant (socket, PSU needs, etc.).\n"
        "Style rules:\n"
        "- Be concise, practical, and consultant-like.\n"
        "- Always reply in the same language as the user's latest message.\n"
        "- If the user writes in Russian, reply in Russian. If in English, reply in English. If in Uzbek, reply in Uzbek.\n"
        "- Do not switch language unless the user asks you to.\n"
        "- Use ONE language only per answer. Never mix two or more languages in one reply.\n"
        "- Do not repeat self-introduction in every answer.\n"
        "- Introduce yourself as BuildBox AI only in the very first assistant message of a chat, or when user asks who you are.\n"
        "- In normal replies, start directly with helpful advice.\n"
        "- Ask 1 short follow-up question when budget/use-case details are missing.\n"
        "- Output plain text only (no Markdown, no **bold**).\n"
        "- Do not write one big paragraph.\n"
        "- Use readable blocks: short intro line, then 2-4 short lines with recommendations, then one short follow-up question.\n"
        "- Keep most answers within 5-8 lines.\n"
        "Refusal template for off-topic questions:\n"
        "- 'I am BuildBox AI, your computer consultant. I can only help with computer and PC topics. Ask me about builds, parts, compatibility, or troubleshooting.'"
    )

    user_payload = json.dumps(
        {
            "question": user_text,
            "catalog": catalog,
            "conversation": conversation,
        },
        ensure_ascii=False,
    )

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    "Use this JSON context from the store and respond strictly by the rules.\n"
                    f"{user_payload}\n\n"
                    f"Long-term memory about this user:\n{memory_summary}"
                ),
            },
        ],
        "temperature": 0.35,
        "max_tokens": 650,
    }

    req = urllib_request.Request(
        url="https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "BuildBox AI Assistant",
        },
        method="POST",
    )

    target_lang = _detect_user_language(user_text)

    try:
        with urllib_request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            choices = data.get("choices") or []
            if choices:
                content = choices[0].get("message", {}).get("content", "")
                if isinstance(content, str) and content.strip():
                    text = _normalize_assistant_text(content)
                    if not _is_response_in_language(text, target_lang):
                        text = _rewrite_to_language(text, target_lang, api_key)
                    return _force_single_language(text, target_lang)
            return "BuildBox AI could not generate a useful answer. Please rephrase your PC question."
    except error.HTTPError as exc:
        if exc.code == 429:
            return "BuildBox AI is temporarily rate-limited. Please try again in a moment."
        return f"BuildBox AI request failed (HTTP {exc.code})."
    except Exception:
        return "BuildBox AI is temporarily unavailable. Please try again in a moment."


PRODUCT_MODEL_MAP = {
    "processor": Processor,
    "gpu": GPU,
    "ram": RAM,
    "motherboard": Motherboard,
    "storage": Storage,
    "powersupply": PowerSupply,
    "case": Case,
    "laptop": Laptop,
}


def _build_product_payload(product, conversation):
    payload = {
        "id": product.pk,
        "model": product._meta.model_name,
        "name": getattr(product, "name", ""),
        "manufacturer": getattr(product, "manufacturer", ""),
        "description": getattr(product, "description", ""),
        "price": float(getattr(product, "price", 0)),
        "stock": int(getattr(product, "stock", 0)),
        "conversation": conversation,
    }
    optional_fields = [
        "socket", "cores", "threads", "base_clock", "boost_clock", "tdp_base", "tdp_max",
        "chipset", "vram", "vram_type", "recommended_psu", "power_consumption", "length",
        "memory_type", "capacity", "modules", "speed", "form_factor", "ram_type",
        "storage_type", "read_speed", "write_speed", "wattage", "efficiency", "modular",
        "processor_name", "gpu_name", "ram_size", "storage_size", "screen_size",
        "screen_resolution", "screen_refresh_rate", "weight", "battery_capacity",
    ]
    for field in optional_fields:
        value = getattr(product, field, None)
        if value not in (None, ""):
            payload[field] = value
    return payload


def _generate_product_ai_reply(user_text, chat_session, product):
    api_key = _get_openrouter_key()
    if not api_key:
        return "AI is not configured yet. Add OPENROUTER_API_KEY, then BuildBox AI Product Assistant will work."

    recent_messages = list(chat_session.messages.order_by("-created_at")[:6])[::-1]
    conversation = [
        {"role": msg.role.lower(), "content": msg.content}
        for msg in recent_messages
        if msg.role in {"USER", "ASSISTANT"}
    ]
    product_payload = _build_product_payload(product, conversation)

    system_prompt = (
        "You are BuildBox AI Product Assistant for a single product page.\n"
        "You can answer ONLY about the current product and directly related compatibility/usage questions.\n"
        "If user asks unrelated things, refuse briefly and bring back to this product.\n"
        "Do not discuss other random products unless comparison is explicitly requested.\n"
        "Never invent specs that are not in provided product JSON.\n"
        "Always reply in the same language as the user's last message.\n"
        "If user writes in Russian, answer in Russian. If English, answer in English. If Uzbek, answer in Uzbek.\n"
        "Never switch language unless user asks to switch.\n"
        "Use ONE language only per answer. Never mix two or more languages in one reply.\n"
        "Use plain text, concise, readable 4-8 lines."
    )

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    "Current product JSON and chat context:\n"
                    f"{json.dumps(product_payload, ensure_ascii=False)}\n\n"
                    f"User question:\n{user_text}"
                ),
            },
        ],
        "temperature": 0.2,
        "max_tokens": 320,
    }

    req = urllib_request.Request(
        url="https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "BuildBox Product Assistant",
        },
        method="POST",
    )

    target_lang = _detect_user_language(user_text)

    try:
        with urllib_request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            choices = data.get("choices") or []
            if choices:
                content = choices[0].get("message", {}).get("content", "")
                if isinstance(content, str) and content.strip():
                    text = _normalize_assistant_text(content)
                    if not _is_response_in_language(text, target_lang):
                        text = _rewrite_to_language(text, target_lang, api_key)
                    return _force_single_language(text, target_lang)
            return "I can only answer about this product. Ask me about specs, compatibility, or usage."
    except error.HTTPError as exc:
        if exc.code == 429:
            return "Product assistant is rate-limited now. Please retry in a moment."
        return f"Product assistant request failed (HTTP {exc.code})."
    except Exception:
        return "Product assistant is temporarily unavailable. Please try again."


@require_GET
def chat_messages(request):
    chat_session = _get_or_create_chat_session(request)
    messages = chat_session.messages.order_by("created_at")
    data = [
        {
            "id": message.id,
            "role": message.role.lower(),
            "content": message.content,
            "created_at": message.created_at.isoformat(),
        }
        for message in messages
    ]
    return JsonResponse({"messages": data})


@require_POST
@csrf_protect
def send_message(request):
    user_text = (request.POST.get("message") or "").strip()
    if not user_text:
        return JsonResponse({"error": "Message is required."}, status=400)

    chat_session = _get_or_create_chat_session(request)
    ChatMessage.objects.create(session=chat_session, role="USER", content=user_text)
    _update_chat_memory(chat_session, user_text)

    assistant_reply = _generate_ai_reply(user_text, chat_session)
    assistant_message = ChatMessage.objects.create(
        session=chat_session,
        role="ASSISTANT",
        content=assistant_reply,
    )

    return JsonResponse(
        {
            "assistant_message": {
                "id": assistant_message.id,
                "role": "assistant",
                "content": assistant_message.content,
                "created_at": assistant_message.created_at.isoformat(),
            }
        }
    )


@require_POST
@csrf_protect
def clear_chat(request):
    chat_session = _get_or_create_chat_session(request)
    chat_session.messages.all().delete()
    return JsonResponse({"ok": True})


@require_GET
def product_chat_messages(request):
    product_model = (request.GET.get("product_model") or "").lower()
    product_id = request.GET.get("product_id")
    if product_model not in PRODUCT_MODEL_MAP or not product_id:
        return JsonResponse({"error": "Invalid product context."}, status=400)

    chat_session = _get_or_create_product_chat_session(request, product_model, product_id)
    messages = chat_session.messages.order_by("created_at")
    data = [
        {
            "id": message.id,
            "role": message.role.lower(),
            "content": message.content,
            "created_at": message.created_at.isoformat(),
        }
        for message in messages
    ]
    return JsonResponse({"messages": data})


@require_POST
@csrf_protect
def product_chat_send(request):
    product_model = (request.POST.get("product_model") or "").lower()
    product_id = request.POST.get("product_id")
    user_text = (request.POST.get("message") or "").strip()

    if product_model not in PRODUCT_MODEL_MAP or not product_id:
        return JsonResponse({"error": "Invalid product context."}, status=400)
    if not user_text:
        return JsonResponse({"error": "Message is required."}, status=400)

    model_cls = PRODUCT_MODEL_MAP[product_model]
    product = get_object_or_404(model_cls, pk=product_id)
    chat_session = _get_or_create_product_chat_session(request, product_model, product_id)
    ChatMessage.objects.create(session=chat_session, role="USER", content=user_text)

    assistant_reply = _generate_product_ai_reply(user_text, chat_session, product)
    assistant_message = ChatMessage.objects.create(
        session=chat_session,
        role="ASSISTANT",
        content=assistant_reply,
    )
    return JsonResponse(
        {
            "assistant_message": {
                "id": assistant_message.id,
                "role": "assistant",
                "content": assistant_message.content,
                "created_at": assistant_message.created_at.isoformat(),
            }
        }
    )


@require_POST
@csrf_protect
def product_chat_clear(request):
    product_model = (request.POST.get("product_model") or "").lower()
    product_id = request.POST.get("product_id")
    if product_model not in PRODUCT_MODEL_MAP or not product_id:
        return JsonResponse({"error": "Invalid product context."}, status=400)
    chat_session = _get_or_create_product_chat_session(request, product_model, product_id)
    chat_session.messages.all().delete()
    return JsonResponse({"ok": True})
