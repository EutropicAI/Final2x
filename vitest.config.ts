import { defineConfig } from 'vitest/config'

export default defineConfig({
  resolve: {
    tsconfigPaths: true,
  },
  test: {
    clearMocks: false,
    projects: [
      {
        extends: true,
        test: {
          name: 'web',
          root: 'test/web',
          include: ['**/*.test.ts'],
          environment: 'jsdom',
        },
      },
      {
        extends: true,
        test: {
          name: 'node',
          root: 'test/node',
          include: ['**/*.test.ts'],
          environment: 'node',
        },
      },
    ],
  },
})
