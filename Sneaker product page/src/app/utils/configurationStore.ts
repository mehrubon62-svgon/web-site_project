export type BuildSlotKey = 'processor' | 'gpu' | 'motherboard' | 'ram' | 'storage' | 'psu' | 'case';

export interface StoredComponent {
  id: string;
  name: string;
  price: number;
  image: string;
  specs: string[];
  manufacturer: string;
}

export interface StoredConfiguration {
  id: string;
  name: string;
  build: Partial<Record<BuildSlotKey, StoredComponent>>;
  totalPrice: number;
  compatibility: 'compatible' | 'warnings' | 'issues';
  createdAt: string;
}

const STORAGE_KEY = 'buildbox.configurations.v1';

export function getSavedConfigurations(): StoredConfiguration[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as StoredConfiguration[];
    if (!Array.isArray(parsed)) return [];
    return parsed;
  } catch {
    return [];
  }
}

export function getSavedConfigurationById(id: string): StoredConfiguration | null {
  return getSavedConfigurations().find(cfg => cfg.id === id) ?? null;
}

export function saveConfiguration(configuration: Omit<StoredConfiguration, 'id' | 'createdAt'>): StoredConfiguration {
  const next: StoredConfiguration = {
    ...configuration,
    id: `cfg-${Date.now()}`,
    createdAt: new Date().toISOString(),
  };

  const current = getSavedConfigurations();
  localStorage.setItem(STORAGE_KEY, JSON.stringify([next, ...current]));
  return next;
}

export function deleteSavedConfiguration(id: string): void {
  const current = getSavedConfigurations();
  localStorage.setItem(STORAGE_KEY, JSON.stringify(current.filter(cfg => cfg.id !== id)));
}
