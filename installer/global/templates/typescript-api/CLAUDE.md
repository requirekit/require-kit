# TypeScript Backend API Project Context for Claude Code

This is a TypeScript Node.js backend API project using NestJS with modern enterprise patterns, functional error handling, and comprehensive testing strategies.

## Technology Stack

- **Framework**: NestJS (Angular-inspired, TypeScript-first)
- **Language**: TypeScript 5.0+ with Node.js 20+ LTS
- **Module System**: ES Modules (modern standard)
- **Error Handling**: Result/Either pattern with `@effect/core` or `ts-results`
- **Testing**: Jest + Supertest + NestJS Testing utilities
- **Validation**: Class-Validator + Class-Transformer with DTOs
- **Documentation**: OpenAPI/Swagger via NestJS Swagger
- **Database**: TypeORM/Prisma with PostgreSQL (configurable)
- **Caching**: Redis for performance optimization
- **Security**: JWT authentication with RBAC authorization

## Project Structure

```
.
├── .claude/                    # Agentic Flow configuration
│   ├── CLAUDE.md              # This file - project context
│   ├── agents/                # Stack-specific agents
│   └── templates/             # Code templates
├── src/
│   ├── modules/               # Feature modules (NestJS style)
│   │   ├── health/           # Health check module
│   │   │   ├── health.controller.ts
│   │   │   ├── health.module.ts
│   │   │   └── health.service.ts
│   │   ├── auth/             # Authentication module
│   │   │   ├── auth.controller.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── auth.module.ts
│   │   │   ├── dto/
│   │   │   │   ├── login.dto.ts
│   │   │   │   └── register.dto.ts
│   │   │   └── guards/
│   │   │       └── jwt-auth.guard.ts
│   │   └── users/            # User management module
│   │       ├── users.controller.ts
│   │       ├── users.service.ts
│   │       ├── users.module.ts
│   │       ├── dto/
│   │       │   ├── create-user.dto.ts
│   │       │   └── update-user.dto.ts
│   │       └── entities/
│   │           └── user.entity.ts
│   ├── common/               # Shared utilities
│   │   ├── decorators/       # Custom decorators
│   │   │   ├── api-response.decorator.ts
│   │   │   └── roles.decorator.ts
│   │   ├── filters/          # Exception filters
│   │   │   ├── http-exception.filter.ts
│   │   │   └── result-exception.filter.ts
│   │   ├── guards/           # Auth guards
│   │   │   ├── roles.guard.ts
│   │   │   └── throttler.guard.ts
│   │   ├── interceptors/     # Request/response interceptors
│   │   │   ├── logging.interceptor.ts
│   │   │   └── transform.interceptor.ts
│   │   ├── pipes/            # Validation pipes
│   │   │   └── validation.pipe.ts
│   │   └── types/            # Shared types and DTOs
│   │       ├── result.type.ts
│   │       └── api-response.type.ts
│   ├── domain/               # Domain layer (DDD approach)
│   │   ├── entities/         # Domain entities
│   │   │   ├── base.entity.ts
│   │   │   └── user.entity.ts
│   │   ├── value-objects/    # Value objects
│   │   │   ├── email.vo.ts
│   │   │   └── user-id.vo.ts
│   │   └── errors/           # Domain-specific errors
│   │       ├── base.error.ts
│   │       ├── user.error.ts
│   │       └── auth.error.ts
│   ├── infrastructure/       # Infrastructure layer
│   │   ├── database/         # Database configuration
│   │   │   ├── database.module.ts
│   │   │   └── migrations/
│   │   ├── external/         # External service clients
│   │   │   └── email.service.ts
│   │   └── config/           # Application configuration
│   │       ├── app.config.ts
│   │       ├── database.config.ts
│   │       └── jwt.config.ts
│   ├── app.module.ts         # Root application module
│   └── main.ts               # Application entry point
├── test/
│   ├── unit/                 # Unit tests
│   │   ├── users/
│   │   │   ├── users.controller.spec.ts
│   │   │   └── users.service.spec.ts
│   │   └── auth/
│   │       ├── auth.controller.spec.ts
│   │       └── auth.service.spec.ts
│   ├── integration/          # Integration tests
│   │   ├── users/
│   │   │   └── users.integration.spec.ts
│   │   └── auth/
│   │       └── auth.integration.spec.ts
│   └── e2e/                  # End-to-end tests
│       ├── app.e2e-spec.ts
│       ├── users.e2e-spec.ts
│       └── auth.e2e-spec.ts
├── docs/                     # Documentation
│   ├── api/                  # API documentation
│   └── architecture/         # Architecture decisions
└── scripts/                  # Utility scripts
    ├── start-dev.sh
    └── test.sh
```

## Development Standards

### TypeScript Configuration
- **Strict Mode**: Enabled for maximum type safety
- **ES Modules**: Modern module system
- **Path Mapping**: Absolute imports for clean code
- **Decorators**: Experimental decorators for NestJS

### Error Handling Pattern (Result/Either)
```typescript
import { Result, Ok, Err } from 'ts-results'

// Service method with explicit error handling
async getUserById(id: string): Promise<Result<User, UserNotFoundError>> {
  try {
    const user = await this.userRepository.findOne({ where: { id } })
    if (!user) {
      return Err(new UserNotFoundError(id))
    }
    return Ok(user)
  } catch (error) {
    return Err(new DatabaseError(error.message))
  }
}

// Controller using Result pattern
@Get(':id')
async findOne(@Param('id') id: string): Promise<ApiResponse<User>> {
  const result = await this.usersService.getUserById(id)

  return result.match(
    user => ({ success: true, data: user }),
    error => { throw new BadRequestException(error.message) }
  )
}
```

### Data Transfer Objects (DTOs)
```typescript
import { IsEmail, IsString, MinLength, IsOptional } from 'class-validator'
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger'

export class CreateUserDto {
  @ApiProperty({ description: 'User email address' })
  @IsEmail()
  email: string

  @ApiProperty({ description: 'User password', minLength: 8 })
  @IsString()
  @MinLength(8)
  password: string

  @ApiPropertyOptional({ description: 'User full name' })
  @IsOptional()
  @IsString()
  fullName?: string
}
```

### Testing Patterns

#### Unit Testing with Jest
```typescript
describe('UsersService', () => {
  let service: UsersService
  let repository: Repository<User>

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: getRepositoryToken(User),
          useClass: Repository,
        },
      ],
    }).compile()

    service = module.get<UsersService>(UsersService)
    repository = module.get<Repository<User>>(getRepositoryToken(User))
  })

  describe('getUserById', () => {
    it('should return user when found', async () => {
      const user = { id: '1', email: 'test@example.com' } as User
      jest.spyOn(repository, 'findOne').mockResolvedValue(user)

      const result = await service.getUserById('1')

      expect(result.ok).toBe(true)
      expect(result.unwrap()).toEqual(user)
    })
  })
})
```

#### E2E Testing with Supertest
```typescript
describe('UsersController (e2e)', () => {
  let app: INestApplication

  beforeEach(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile()

    app = moduleFixture.createNestApplication()
    await app.init()
  })

  it('/users (GET)', () => {
    return request(app.getHttpServer())
      .get('/users')
      .expect(200)
      .expect(res => {
        expect(res.body.success).toBe(true)
        expect(Array.isArray(res.body.data)).toBe(true)
      })
  })
})
```

## NuGet/NPM Packages Required

```json
{
  "dependencies": {
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "@nestjs/platform-express": "^10.0.0",
    "@nestjs/typeorm": "^10.0.0",
    "@nestjs/jwt": "^10.0.0",
    "@nestjs/passport": "^10.0.0",
    "@nestjs/swagger": "^7.0.0",
    "@nestjs/throttler": "^5.0.0",
    "class-validator": "^0.14.0",
    "class-transformer": "^0.5.1",
    "typeorm": "^0.3.17",
    "pg": "^8.11.0",
    "redis": "^4.6.0",
    "passport": "^0.7.0",
    "passport-jwt": "^4.0.1",
    "bcrypt": "^5.1.0",
    "ts-results": "^3.3.0",
    "reflect-metadata": "^0.1.13",
    "rxjs": "^7.8.1"
  },
  "devDependencies": {
    "@nestjs/cli": "^10.0.0",
    "@nestjs/schematics": "^10.0.0",
    "@nestjs/testing": "^10.0.0",
    "@types/express": "^4.17.17",
    "@types/jest": "^29.5.2",
    "@types/node": "^20.3.1",
    "@types/passport-jwt": "^3.0.9",
    "@types/bcrypt": "^5.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.42.0",
    "eslint-config-prettier": "^9.0.0",
    "eslint-plugin-prettier": "^5.0.0",
    "jest": "^29.5.0",
    "prettier": "^3.0.0",
    "supertest": "^6.3.3",
    "ts-jest": "^29.1.0",
    "ts-loader": "^9.4.3",
    "ts-node": "^10.9.1",
    "tsconfig-paths": "^4.2.0",
    "typescript": "^5.1.3"
  }
}
```

## Development Commands

### Build and Run
```bash
# Development with hot reload
npm run start:dev

# Production build
npm run build
npm run start:prod

# Debug mode
npm run start:debug
```

### Testing
```bash
# Run all tests
npm test

# Unit tests only
npm run test:unit

# E2E tests
npm run test:e2e

# Test coverage
npm run test:cov

# Watch mode
npm run test:watch
```

### Code Quality
```bash
# Lint code
npm run lint

# Format code
npm run format

# Type checking
npm run type-check
```

## API Documentation

### Swagger/OpenAPI Integration
- **URL**: `/api/docs` (development)
- **Authentication**: JWT Bearer tokens
- **Response Format**: Standardized API response wrapper
- **Error Codes**: HTTP status codes with detailed error messages

### Response Format
```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: {
    code: string
    message: string
    details?: unknown
  }
  meta?: {
    page?: number
    limit?: number
    total?: number
  }
}
```

## Security Standards

### Authentication & Authorization
- **JWT Tokens**: Access and refresh token strategy
- **Password Hashing**: bcrypt with salt rounds
- **Role-Based Access Control**: Decorator-based permissions
- **Rate Limiting**: Redis-backed throttling

### Input Validation
- **DTO Validation**: Class-validator decorators
- **Sanitization**: Automatic input sanitization
- **Type Safety**: Strong TypeScript typing throughout

## Performance Requirements
- **API Response Time**: < 200ms for standard endpoints
- **Database Queries**: Optimized with proper indexing
- **Caching Strategy**: Redis for frequently accessed data
- **Memory Usage**: < 512MB for typical workloads

## Quality Gates (Automatic)
- **Test Coverage**: ≥ 85% line coverage, ≥ 80% branch coverage
- **Type Safety**: Zero `any` types in production code
- **Code Quality**: ESLint score > 8.5/10
- **Security**: No high/critical security vulnerabilities
- **Performance**: All endpoints < 200ms response time

## Best Practices

### 1. **Modular Architecture**
- Organize code by feature modules
- Keep modules loosely coupled
- Use dependency injection consistently

### 2. **Error Handling**
- Use Result/Either pattern for explicit error handling
- Create domain-specific error types
- Implement global exception filters

### 3. **Testing Strategy**
- Follow testing pyramid: 70% unit, 20% integration, 10% e2e
- Mock external dependencies in unit tests
- Use test containers for integration tests

### 4. **Security First**
- Validate all inputs at API boundary
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization

### 5. **Performance Optimization**
- Use caching strategically
- Implement database query optimization
- Monitor and log performance metrics

## Common Patterns

### Controller Pattern
```typescript
@Controller('users')
@UseGuards(JwtAuthGuard)
@ApiTags('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  @Roles(Role.Admin)
  @UseGuards(RolesGuard)
  async create(@Body() createUserDto: CreateUserDto): Promise<ApiResponse<User>> {
    const result = await this.usersService.create(createUserDto)

    return result.match(
      user => ({ success: true, data: user }),
      error => { throw new BadRequestException(error.message) }
    )
  }
}
```

### Service Pattern with Result
```typescript
@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private readonly userRepository: Repository<User>,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<Result<User, UserCreationError>> {
    try {
      const existingUser = await this.userRepository.findOne({
        where: { email: createUserDto.email }
      })

      if (existingUser) {
        return Err(new UserAlreadyExistsError(createUserDto.email))
      }

      const user = this.userRepository.create(createUserDto)
      const savedUser = await this.userRepository.save(user)

      return Ok(savedUser)
    } catch (error) {
      return Err(new DatabaseError(error.message))
    }
  }
}
```

## Available Commands

### NestJS-Specific Commands
Use `/create-module ModuleName` to generate:
- Module with controller, service, and DTOs
- Complete CRUD operations with Result pattern
- Unit and integration tests
- Swagger documentation

Use `/create-entity EntityName` to generate:
- TypeORM entity with proper decorators
- Domain model with validation
- Repository pattern implementation
- Migration files

Use `/create-guard GuardName` to generate:
- Custom guard implementation
- Role-based authorization logic
- Unit tests for guard behavior

## Workflow Integration

### Requirements → Implementation Flow
1. **Gather Requirements** (`/gather-requirements`)
   - Creates docs/requirements/draft/feature.md

2. **Formalize to EARS** (`/formalize-ears`)
   - Moves to docs/requirements/approved/feature.md

3. **Generate BDD** (`/generate-bdd`)
   - Creates docs/bdd/features/feature.feature

4. **Implement Feature**
   - Create module with NestJS CLI patterns
   - Implement services with Result pattern
   - Create controllers with proper decorators
   - Write comprehensive tests

5. **Update State** (`/update-state`)
   - Move to docs/requirements/implemented/
   - Update docs/state/current-sprint.md

## Resources
- [NestJS Documentation](https://docs.nestjs.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Jest Testing Framework](https://jestjs.io/docs/getting-started)
- [TypeORM Documentation](https://typeorm.io/)
- [Result Pattern Library](https://github.com/vultix/ts-results)
- [Class Validator](https://github.com/typestack/class-validator)