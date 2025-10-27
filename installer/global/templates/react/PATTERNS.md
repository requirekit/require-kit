# React Advanced Patterns

This document contains advanced patterns and best practices learned from production React applications.

## Error Handling Patterns

### Error Boundaries
```typescript
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = { hasError: false };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
    // Send to error reporting service
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || <h1>Something went wrong.</h1>;
    }

    return this.props.children;
  }
}
```

### API Error Handling
```typescript
export interface ApiError {
  code: string;
  message: string;
  details?: unknown;
  timestamp: string;
}

export class ApiClient {
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error: ApiError = {
        code: `HTTP_${response.status}`,
        message: response.statusText,
        timestamp: new Date().toISOString(),
      };
      
      try {
        const data = await response.json();
        error.details = data;
      } catch {}
      
      throw error;
    }
    
    return response.json();
  }
  
  async get<T>(url: string): Promise<T> {
    try {
      const response = await fetch(url);
      return this.handleResponse<T>(response);
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }
}
```

### Retry Logic
```typescript
export async function withRetry<T>(
  fn: () => Promise<T>,
  options = { maxRetries: 3, delay: 1000 }
): Promise<T> {
  let lastError: Error;
  
  for (let i = 0; i <= options.maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      if (i < options.maxRetries) {
        await new Promise(resolve => 
          setTimeout(resolve, options.delay * Math.pow(2, i))
        );
      }
    }
  }
  
  throw lastError!;
}
```

## State Management Patterns

### Local State with useReducer
```typescript
type State = {
  loading: boolean;
  data: Data | null;
  error: Error | null;
};

type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: Data }
  | { type: 'FETCH_ERROR'; payload: Error };

function dataReducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, loading: true, error: null };
    case 'FETCH_SUCCESS':
      return { loading: false, data: action.payload, error: null };
    case 'FETCH_ERROR':
      return { ...state, loading: false, error: action.payload };
    default:
      return state;
  }
}

export function useDataFetch(url: string) {
  const [state, dispatch] = useReducer(dataReducer, {
    loading: false,
    data: null,
    error: null,
  });
  
  useEffect(() => {
    let cancelled = false;
    
    async function fetchData() {
      dispatch({ type: 'FETCH_START' });
      
      try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (!cancelled) {
          dispatch({ type: 'FETCH_SUCCESS', payload: data });
        }
      } catch (error) {
        if (!cancelled) {
          dispatch({ type: 'FETCH_ERROR', payload: error as Error });
        }
      }
    }
    
    fetchData();
    
    return () => {
      cancelled = true;
    };
  }, [url]);
  
  return state;
}
```

### Context Pattern for Global State
```typescript
interface AppState {
  user: User | null;
  theme: 'light' | 'dark';
  notifications: Notification[];
}

interface AppContextValue {
  state: AppState;
  actions: {
    setUser: (user: User | null) => void;
    setTheme: (theme: 'light' | 'dark') => void;
    addNotification: (notification: Notification) => void;
    removeNotification: (id: string) => void;
  };
}

const AppContext = createContext<AppContextValue | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AppState>({
    user: null,
    theme: 'light',
    notifications: [],
  });
  
  const actions = useMemo(() => ({
    setUser: (user: User | null) => 
      setState(prev => ({ ...prev, user })),
    setTheme: (theme: 'light' | 'dark') => 
      setState(prev => ({ ...prev, theme })),
    addNotification: (notification: Notification) =>
      setState(prev => ({ 
        ...prev, 
        notifications: [...prev.notifications, notification] 
      })),
    removeNotification: (id: string) =>
      setState(prev => ({
        ...prev,
        notifications: prev.notifications.filter(n => n.id !== id)
      })),
  }), []);
  
  const value = useMemo(() => ({ state, actions }), [state, actions]);
  
  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
}
```

## API Integration Patterns

### API Client Factory
```typescript
interface ApiClientConfig {
  baseURL: string;
  headers?: Record<string, string>;
  timeout?: number;
}

export class ApiClient {
  private config: ApiClientConfig;
  private abortControllers = new Map<string, AbortController>();
  
  constructor(config: ApiClientConfig) {
    this.config = config;
  }
  
  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    requestId?: string
  ): Promise<T> {
    // Cancel previous request with same ID
    if (requestId) {
      this.cancel(requestId);
      const controller = new AbortController();
      this.abortControllers.set(requestId, controller);
      options.signal = controller.signal;
    }
    
    const url = `${this.config.baseURL}${endpoint}`;
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...this.config.headers,
        ...options.headers,
      },
    };
    
    if (this.config.timeout) {
      const timeoutId = setTimeout(() => {
        if (requestId) this.cancel(requestId);
      }, this.config.timeout);
      
      try {
        const response = await fetch(url, config);
        clearTimeout(timeoutId);
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
      } catch (error) {
        clearTimeout(timeoutId);
        throw error;
      }
    }
    
    const response = await fetch(url, config);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return response.json();
  }
  
  cancel(requestId: string) {
    const controller = this.abortControllers.get(requestId);
    if (controller) {
      controller.abort();
      this.abortControllers.delete(requestId);
    }
  }
  
  cancelAll() {
    this.abortControllers.forEach(controller => controller.abort());
    this.abortControllers.clear();
  }
  
  get<T>(endpoint: string, requestId?: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' }, requestId);
  }
  
  post<T>(endpoint: string, data?: unknown, requestId?: string): Promise<T> {
    return this.request<T>(
      endpoint,
      {
        method: 'POST',
        body: data ? JSON.stringify(data) : undefined,
      },
      requestId
    );
  }
}

// Usage
const apiClient = new ApiClient({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:3000',
  timeout: 30000,
});

export default apiClient;
```

### Server-Sent Events (SSE) Hook
```typescript
export interface UseSSEOptions {
  onMessage?: (data: any) => void;
  onError?: (error: Error) => void;
  onOpen?: () => void;
  onClose?: () => void;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
}

export function useSSE(url: string, options: UseSSEOptions = {}) {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<Error | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);
  const reconnectAttemptsRef = useRef(0);
  
  const connect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }
    
    const eventSource = new EventSource(url);
    eventSourceRef.current = eventSource;
    
    eventSource.onopen = () => {
      setIsConnected(true);
      setError(null);
      reconnectAttemptsRef.current = 0;
      options.onOpen?.();
    };
    
    eventSource.onmessage = (event) => {
      try {
        const parsedData = JSON.parse(event.data);
        setData(parsedData);
        options.onMessage?.(parsedData);
      } catch (err) {
        console.error('Failed to parse SSE data:', err);
      }
    };
    
    eventSource.onerror = (err) => {
      setIsConnected(false);
      setError(new Error('SSE connection failed'));
      options.onError?.(new Error('SSE connection failed'));
      
      // Reconnect logic
      const maxAttempts = options.maxReconnectAttempts ?? 5;
      if (reconnectAttemptsRef.current < maxAttempts) {
        reconnectAttemptsRef.current++;
        setTimeout(connect, options.reconnectInterval ?? 1000);
      }
    };
  }, [url, options]);
  
  useEffect(() => {
    connect();
    
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, [connect]);
  
  const disconnect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
      setIsConnected(false);
    }
  }, []);
  
  return {
    data,
    error,
    isConnected,
    disconnect,
    reconnect: connect,
  };
}
```

## Form Handling Patterns

### Controlled Form with Validation
```typescript
interface FormData {
  email: string;
  password: string;
}

interface FormErrors {
  email?: string;
  password?: string;
}

export function useForm<T extends Record<string, any>>(
  initialValues: T,
  validate?: (values: T) => Partial<Record<keyof T, string>>
) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const { name, value, type, checked } = e.target;
      setValues(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value,
      }));
    },
    []
  );
  
  const handleBlur = useCallback(
    (e: React.FocusEvent<HTMLInputElement>) => {
      const { name } = e.target;
      setTouched(prev => ({ ...prev, [name]: true }));
      
      if (validate) {
        const validationErrors = validate(values);
        setErrors(validationErrors);
      }
    },
    [values, validate]
  );
  
  const handleSubmit = useCallback(
    async (onSubmit: (values: T) => Promise<void>) => {
      return async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (validate) {
          const validationErrors = validate(values);
          setErrors(validationErrors);
          
          if (Object.keys(validationErrors).length > 0) {
            return;
          }
        }
        
        setIsSubmitting(true);
        
        try {
          await onSubmit(values);
        } catch (error) {
          console.error('Form submission error:', error);
        } finally {
          setIsSubmitting(false);
        }
      };
    },
    [values, validate]
  );
  
  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  }, [initialValues]);
  
  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    reset,
    setFieldValue: (name: keyof T, value: any) => 
      setValues(prev => ({ ...prev, [name]: value })),
    setFieldError: (name: keyof T, error: string) =>
      setErrors(prev => ({ ...prev, [name]: error })),
  };
}
```

## Accessibility Patterns

### Focus Management
```typescript
export function useFocusTrap(containerRef: RefObject<HTMLElement>) {
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    
    const focusableElements = container.querySelectorAll(
      'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
    );
    
    const firstFocusable = focusableElements[0] as HTMLElement;
    const lastFocusable = focusableElements[focusableElements.length - 1] as HTMLElement;
    
    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;
      
      if (e.shiftKey) {
        if (document.activeElement === firstFocusable) {
          lastFocusable.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastFocusable) {
          firstFocusable.focus();
          e.preventDefault();
        }
      }
    };
    
    container.addEventListener('keydown', handleTabKey);
    firstFocusable?.focus();
    
    return () => {
      container.removeEventListener('keydown', handleTabKey);
    };
  }, [containerRef]);
}
```

### Announcements for Screen Readers
```typescript
export function useAnnounce() {
  const [announcement, setAnnouncement] = useState('');
  
  const announce = useCallback((message: string, priority: 'polite' | 'assertive' = 'polite') => {
    setAnnouncement('');
    setTimeout(() => {
      setAnnouncement(message);
    }, 100);
  }, []);
  
  return {
    announcement,
    announce,
    Announcer: () => (
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {announcement}
      </div>
    ),
  };
}
```

## Performance Optimization Patterns

### Debouncing and Throttling
```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);
  
  return debouncedValue;
}

export function useThrottle<T>(value: T, interval: number): T {
  const [throttledValue, setThrottledValue] = useState<T>(value);
  const lastUpdated = useRef<number>(Date.now());
  
  useEffect(() => {
    const now = Date.now();
    const timeSinceLastUpdate = now - lastUpdated.current;
    
    if (timeSinceLastUpdate >= interval) {
      lastUpdated.current = now;
      setThrottledValue(value);
    } else {
      const timer = setTimeout(() => {
        lastUpdated.current = Date.now();
        setThrottledValue(value);
      }, interval - timeSinceLastUpdate);
      
      return () => clearTimeout(timer);
    }
  }, [value, interval]);
  
  return throttledValue;
}
```

### Virtual Scrolling
```typescript
export function useVirtualScroll<T>({
  items,
  itemHeight,
  containerHeight,
  overscan = 3,
}: {
  items: T[];
  itemHeight: number;
  containerHeight: number;
  overscan?: number;
}) {
  const [scrollTop, setScrollTop] = useState(0);
  
  const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan);
  const endIndex = Math.min(
    items.length - 1,
    Math.ceil((scrollTop + containerHeight) / itemHeight) + overscan
  );
  
  const visibleItems = items.slice(startIndex, endIndex + 1);
  const totalHeight = items.length * itemHeight;
  const offsetY = startIndex * itemHeight;
  
  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(e.currentTarget.scrollTop);
  }, []);
  
  return {
    visibleItems,
    totalHeight,
    offsetY,
    handleScroll,
  };
}
```

## Security Patterns

### Input Sanitization
```typescript
export function useSanitizedInput(
  initialValue: string,
  sanitizer?: (value: string) => string
) {
  const [value, setValue] = useState(initialValue);
  const [sanitizedValue, setSanitizedValue] = useState(initialValue);
  
  const defaultSanitizer = (input: string) => {
    // Remove script tags and dangerous attributes
    return input
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
      .replace(/on\w+="[^"]*"/g, '')
      .replace(/on\w+='[^']*'/g, '');
  };
  
  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setValue(newValue);
    
    const sanitize = sanitizer || defaultSanitizer;
    setSanitizedValue(sanitize(newValue));
  }, [sanitizer]);
  
  return {
    value,
    sanitizedValue,
    handleChange,
  };
}
```

### Secure Storage
```typescript
export class SecureStorage {
  private encrypt(data: string): string {
    // In production, use a proper encryption library
    return btoa(data);
  }
  
  private decrypt(data: string): string {
    // In production, use a proper decryption library
    return atob(data);
  }
  
  setItem(key: string, value: any): void {
    const encrypted = this.encrypt(JSON.stringify(value));
    localStorage.setItem(key, encrypted);
  }
  
  getItem<T>(key: string): T | null {
    const encrypted = localStorage.getItem(key);
    if (!encrypted) return null;
    
    try {
      const decrypted = this.decrypt(encrypted);
      return JSON.parse(decrypted);
    } catch {
      return null;
    }
  }
  
  removeItem(key: string): void {
    localStorage.removeItem(key);
  }
  
  clear(): void {
    localStorage.clear();
  }
}

export const secureStorage = new SecureStorage();
```

## Best Practices Summary

1. **Always handle loading, error, and success states** in data fetching
2. **Use AbortController** to cancel requests when components unmount
3. **Implement retry logic** with exponential backoff for network failures
4. **Memoize expensive computations** and callback functions
5. **Use error boundaries** to catch and handle React errors gracefully
6. **Implement proper TypeScript types** for all props and state
7. **Follow accessibility guidelines** (WCAG 2.1 AA minimum)
8. **Optimize bundle size** with code splitting and lazy loading
9. **Use proper form validation** with clear error messages
10. **Implement proper security measures** for user input and storage
