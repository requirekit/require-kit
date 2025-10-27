# React Template - AI Engineer

## Overview

This React template has been enhanced with production-ready patterns and best practices learned from real-world implementations. It provides a comprehensive foundation for building robust, scalable React applications with TypeScript.

## Key Improvements

### 1. Enhanced Project Structure
- **Organized component hierarchy**: `ui/`, `features/`, and `layout/` subdirectories for better component organization
- **Service layer pattern**: Separate API services with proper error handling and retry logic
- **Design tokens system**: Centralized design system configuration
- **Context organization**: Dedicated contexts folder for global state management

### 2. Advanced Testing Patterns
- **Comprehensive test coverage**: Unit, integration, E2E, and accessibility testing
- **User interaction testing**: Using `@testing-library/user-event` for realistic user interactions
- **Accessibility testing**: Built-in `jest-axe` integration for WCAG compliance
- **Performance testing**: Memoization and debouncing test patterns

### 3. Error Handling & Resilience
- **Error boundaries**: Graceful error handling at component level
- **API error handling**: Structured error responses with retry logic
- **Abort controllers**: Proper request cancellation for cleanup
- **Fallback strategies**: Progressive degradation patterns

### 4. Performance Optimizations
- **React.memo patterns**: Intelligent component memoization
- **useMemo/useCallback**: Proper hook optimization patterns
- **Debouncing/Throttling**: Built-in performance utilities
- **Virtual scrolling**: Patterns for large list rendering
- **Bundle optimization**: Code splitting and lazy loading strategies

### 5. API Integration Patterns
- **API Client Factory**: Reusable, configurable API client
- **Server-Sent Events (SSE)**: Real-time streaming patterns with reconnection
- **Request cancellation**: AbortController integration
- **Caching strategies**: Built-in cache management
- **Batch operations**: Support for batch API calls

### 6. State Management
- **Local state patterns**: useReducer for complex state logic
- **Context patterns**: Optimized global state with proper memoization
- **Form handling**: Comprehensive form state management with validation
- **Async state**: Loading, error, and success state handling

### 7. Accessibility Features
- **Focus management**: useFocusTrap for modal/dialog accessibility
- **Screen reader announcements**: Live region updates
- **Keyboard navigation**: Comprehensive keyboard support patterns
- **ARIA attributes**: Proper semantic HTML and ARIA usage

### 8. Security Patterns
- **Input sanitization**: Protection against XSS attacks
- **Secure storage**: Encrypted local storage patterns
- **API security**: Proper authentication header handling
- **CORS handling**: Correct CORS configuration patterns

## Template Files

### Component Template (`component.tsx.hbs`)
- TypeScript interfaces with JSDoc comments
- Accessibility-first implementation
- Proper prop handling and default values
- Memoization ready structure

### Component Test Template (`component.test.tsx.hbs`)
- Comprehensive test scenarios
- Accessibility testing included
- Performance testing patterns
- Snapshot testing setup

### Hook Template (`hook.ts.hbs`)
- Cancellable async operations
- Proper cleanup on unmount
- Caching support
- Debouncing capabilities

### Service Template (`service.ts.hbs`)
- Retry logic with exponential backoff
- Request cancellation
- Runtime validation with Zod
- Streaming support (SSE)

## Usage

### Creating a New Component
```bash
/create-component MyComponent
```
This generates:
- `MyComponent/index.ts`
- `MyComponent/MyComponent.tsx`
- `MyComponent/MyComponent.types.ts`
- `MyComponent/MyComponent.test.tsx`

### Creating a Custom Hook
```bash
/create-hook useMyHook
```
Generates a fully-featured hook with:
- TypeScript types
- Cancellation support
- Error handling
- Memoization

### Creating a Service
```bash
/create-service UserService
```
Creates an API service with:
- Retry logic
- Error handling
- Type validation
- Request cancellation

## Best Practices

### Component Development
1. Always include proper TypeScript types
2. Implement error boundaries for critical components
3. Use semantic HTML and ARIA attributes
4. Memoize expensive computations
5. Include comprehensive tests

### Performance
1. Use React.memo for expensive components
2. Implement proper useCallback/useMemo usage
3. Lazy load routes and heavy components
4. Monitor bundle size regularly
5. Use virtual scrolling for large lists

### Testing
1. Test user interactions, not implementation details
2. Include accessibility tests for all components
3. Mock external dependencies properly
4. Test error states and edge cases
5. Use snapshot tests sparingly

### Security
1. Sanitize all user inputs
2. Use HTTPS for all API calls
3. Implement proper authentication
4. Never store sensitive data in localStorage
5. Validate all API responses

## Configuration

### TypeScript Configuration
The template enforces strict TypeScript settings:
- `strict: true`
- `noImplicitAny: true`
- `strictNullChecks: true`

### ESLint Rules
Includes rules for:
- Complexity limits (max 10)
- File size limits (300 lines)
- Accessibility requirements
- React best practices

### Performance Targets
- Core Web Vitals compliance
- Bundle size < 150KB initial
- 60fps rendering (16ms budget)
- Zero memory leaks

## Additional Resources

- See `PATTERNS.md` for advanced React patterns
- Check `CLAUDE.md` for AI-assisted development guidelines
- Review test examples in template files
- Refer to service patterns for API integration

## Contributing

When adding new patterns or templates:
1. Ensure they follow existing conventions
2. Include comprehensive tests
3. Document the pattern in appropriate files
4. Consider performance implications
5. Maintain accessibility standards

## License

MIT