import { defineConfig } from 'orval';

export default defineConfig({
	api: {
		input: 'http://127.0.0.1:8000/openapi.json',
		output: {
			mode: 'split',
			target: './src/lib/api/generated/endpoints.ts',
			schemas: './src/lib/api/generated/model',
			client: 'svelte-query',
			override: {
				mutator: {
					path: './src/lib/api/axios.ts',
					name: 'customInstance'
				}
			}
		}
	}
});
