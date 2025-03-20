import { setupServer } from 'msw/node';
import { rest } from 'msw';

const handlers = [
  // Auth endpoints
  rest.post('/api/auth/login', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        user: {
          id: '1',
          email: 'test@example.com',
          name: 'Test User',
          role: 'dispatcher',
        },
        token: 'mock-jwt-token',
      })
    );
  }),

  rest.get('/api/auth/me', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        id: '1',
        email: 'test@example.com',
        name: 'Test User',
        role: 'dispatcher',
      })
    );
  }),

  // Alert endpoints
  rest.get('/api/alerts', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          id: '1',
          type: 'fire',
          severity: 'high',
          status: 'pending',
          location: {
            latitude: 40.7128,
            longitude: -74.0060,
            address: 'New York, NY',
          },
          description: 'Test alert',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        },
      ])
    );
  }),

  rest.post('/api/alerts/:id/status', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        id: '1',
        type: 'fire',
        severity: 'high',
        status: 'assigned',
        location: {
          latitude: 40.7128,
          longitude: -74.0060,
          address: 'New York, NY',
        },
        description: 'Test alert',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      })
    );
  }),

  // Team endpoints
  rest.get('/api/teams', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          id: '1',
          name: 'Team A',
          members: [],
          status: 'available',
        },
      ])
    );
  }),

  // User endpoints
  rest.get('/api/users', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          id: '1',
          email: 'test@example.com',
          name: 'Test User',
          role: 'dispatcher',
        },
      ])
    );
  }),
];

export const server = setupServer(...handlers); 