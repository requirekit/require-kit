// src/common/types/api-response.type.ts

import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

/**
 * Standard API response wrapper
 */
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: ApiError;
  meta?: ApiMeta;
}

/**
 * API error structure
 */
export interface ApiError {
  code: string;
  message: string;
  details?: unknown;
  timestamp?: string;
  path?: string;
  method?: string;
}

/**
 * API metadata for pagination and additional info
 */
export interface ApiMeta {
  page?: number;
  limit?: number;
  total?: number;
  totalPages?: number;
  hasNext?: boolean;
  hasPrevious?: boolean;
  requestId?: string;
  version?: string;
}

/**
 * Success response DTO for Swagger documentation
 */
export class SuccessResponseDto<T> {
  @ApiProperty({ example: true })
  success: boolean;

  @ApiProperty()
  data: T;

  @ApiPropertyOptional()
  meta?: ApiMeta;
}

/**
 * Error response DTO for Swagger documentation
 */
export class ErrorResponseDto {
  @ApiProperty({ example: false })
  success: boolean;

  @ApiProperty({
    example: {
      code: 'VALIDATION_ERROR',
      message: 'Invalid input data',
      timestamp: '2024-01-01T00:00:00.000Z',
      path: '/users',
      method: 'POST'
    }
  })
  error: ApiError;
}

/**
 * Paginated response DTO for Swagger documentation
 */
export class PaginatedResponseDto<T> {
  @ApiProperty({ example: true })
  success: boolean;

  @ApiProperty({ isArray: true })
  data: T[];

  @ApiProperty({
    example: {
      page: 1,
      limit: 10,
      total: 100,
      totalPages: 10,
      hasNext: true,
      hasPrevious: false
    }
  })
  meta: ApiMeta;
}

/**
 * Utility functions for creating API responses
 */
export class ApiResponseBuilder {
  /**
   * Create success response
   */
  static success<T>(data: T, meta?: ApiMeta): ApiResponse<T> {
    return {
      success: true,
      data,
      meta
    };
  }

  /**
   * Create error response
   */
  static error(
    code: string,
    message: string,
    details?: unknown,
    path?: string,
    method?: string
  ): ApiResponse {
    return {
      success: false,
      error: {
        code,
        message,
        details,
        timestamp: new Date().toISOString(),
        path,
        method
      }
    };
  }

  /**
   * Create paginated response
   */
  static paginated<T>(
    data: T[],
    page: number,
    limit: number,
    total: number
  ): ApiResponse<T[]> {
    const totalPages = Math.ceil(total / limit);
    const hasNext = page < totalPages;
    const hasPrevious = page > 1;

    return {
      success: true,
      data,
      meta: {
        page,
        limit,
        total,
        totalPages,
        hasNext,
        hasPrevious
      }
    };
  }

  /**
   * Create empty success response (for delete operations)
   */
  static deleted(): ApiResponse {
    return {
      success: true
    };
  }

  /**
   * Create created response
   */
  static created<T>(data: T): ApiResponse<T> {
    return {
      success: true,
      data
    };
  }

  /**
   * Create updated response
   */
  static updated<T>(data: T): ApiResponse<T> {
    return {
      success: true,
      data
    };
  }
}

/**
 * Pagination parameters DTO
 */
export class PaginationDto {
  @ApiPropertyOptional({
    description: 'Page number (1-based)',
    example: 1,
    minimum: 1,
    default: 1
  })
  page?: number = 1;

  @ApiPropertyOptional({
    description: 'Number of items per page',
    example: 10,
    minimum: 1,
    maximum: 100,
    default: 10
  })
  limit?: number = 10;

  @ApiPropertyOptional({
    description: 'Sort field',
    example: 'createdAt'
  })
  sortBy?: string;

  @ApiPropertyOptional({
    description: 'Sort order',
    example: 'DESC',
    enum: ['ASC', 'DESC']
  })
  sortOrder?: 'ASC' | 'DESC' = 'DESC';

  /**
   * Get skip value for database queries
   */
  getSkip(): number {
    return (this.page! - 1) * this.limit!;
  }

  /**
   * Get take value for database queries
   */
  getTake(): number {
    return this.limit!;
  }
}