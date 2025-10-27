// src/domain/errors/base.error.ts

/**
 * Base domain error class
 * All domain errors should extend this class
 */
export abstract class DomainError extends Error {
  abstract readonly code: string;
  abstract readonly type: 'validation' | 'business' | 'infrastructure';

  constructor(message: string, cause?: Error) {
    super(message);
    this.name = this.constructor.name;
    this.cause = cause;

    // Maintains proper stack trace for where our error was thrown (only available on V8)
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, this.constructor);
    }
  }

  /**
   * Convert error to JSON representation
   */
  toJSON(): Record<string, unknown> {
    return {
      name: this.name,
      code: this.code,
      type: this.type,
      message: this.message,
      stack: this.stack
    };
  }

  /**
   * Get error details for logging
   */
  getDetails(): Record<string, unknown> {
    return {
      code: this.code,
      type: this.type,
      message: this.message
    };
  }
}

/**
 * Validation error - for input validation failures
 */
export class ValidationError extends DomainError {
  readonly type = 'validation' as const;
  readonly code = 'VALIDATION_ERROR';

  constructor(message: string, public readonly field?: string) {
    super(message);
  }

  getDetails(): Record<string, unknown> {
    return {
      ...super.getDetails(),
      field: this.field
    };
  }
}

/**
 * Business rule error - for domain business rule violations
 */
export class BusinessRuleError extends DomainError {
  readonly type = 'business' as const;
  readonly code = 'BUSINESS_RULE_ERROR';

  constructor(message: string, public readonly rule?: string) {
    super(message);
  }

  getDetails(): Record<string, unknown> {
    return {
      ...super.getDetails(),
      rule: this.rule
    };
  }
}

/**
 * Infrastructure error - for external service failures
 */
export class InfrastructureError extends DomainError {
  readonly type = 'infrastructure' as const;
  readonly code = 'INFRASTRUCTURE_ERROR';

  constructor(message: string, public readonly service?: string, cause?: Error) {
    super(message, cause);
  }

  getDetails(): Record<string, unknown> {
    return {
      ...super.getDetails(),
      service: this.service
    };
  }
}

/**
 * Database error - for database operation failures
 */
export class DatabaseError extends InfrastructureError {
  readonly code = 'DATABASE_ERROR';

  constructor(message: string, cause?: Error) {
    super(message, 'database', cause);
  }
}

/**
 * External API error - for external API failures
 */
export class ExternalApiError extends InfrastructureError {
  readonly code = 'EXTERNAL_API_ERROR';

  constructor(message: string, public readonly apiName: string, cause?: Error) {
    super(message, apiName, cause);
  }

  getDetails(): Record<string, unknown> {
    return {
      ...super.getDetails(),
      apiName: this.apiName
    };
  }
}

/**
 * Authentication error - for authentication failures
 */
export class AuthenticationError extends DomainError {
  readonly type = 'business' as const;
  readonly code = 'AUTHENTICATION_ERROR';

  constructor(message: string = 'Authentication failed') {
    super(message);
  }
}

/**
 * Authorization error - for authorization failures
 */
export class AuthorizationError extends DomainError {
  readonly type = 'business' as const;
  readonly code = 'AUTHORIZATION_ERROR';

  constructor(message: string = 'Access denied') {
    super(message);
  }
}

/**
 * Not found error - for resource not found scenarios
 */
export class NotFoundError extends DomainError {
  readonly type = 'business' as const;
  readonly code = 'NOT_FOUND_ERROR';

  constructor(resource: string, identifier?: string) {
    const message = identifier
      ? `${resource} with identifier '${identifier}' not found`
      : `${resource} not found`;
    super(message);
  }
}

/**
 * Conflict error - for resource conflict scenarios
 */
export class ConflictError extends DomainError {
  readonly type = 'business' as const;
  readonly code = 'CONFLICT_ERROR';

  constructor(message: string) {
    super(message);
  }
}

/**
 * Rate limit error - for rate limiting scenarios
 */
export class RateLimitError extends DomainError {
  readonly type = 'business' as const;
  readonly code = 'RATE_LIMIT_ERROR';

  constructor(message: string = 'Rate limit exceeded', public readonly retryAfter?: number) {
    super(message);
  }

  getDetails(): Record<string, unknown> {
    return {
      ...super.getDetails(),
      retryAfter: this.retryAfter
    };
  }
}