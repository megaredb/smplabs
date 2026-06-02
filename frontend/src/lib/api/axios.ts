// Custom fetch-based instance for Orval-generated code.
// Signature matches what Orval's svelte-query client expects: (url, options?) => Promise<T>
export const customInstance = async <T>(url: string, options?: RequestInit): Promise<T> => {
	// Merge headers: start from provided headers (which may include Content-Type set by Orval)
	const baseHeaders: Record<string, string> = {};

	// Inject auth token
	if (typeof window !== 'undefined') {
		const token = localStorage.getItem('access_token');
		if (token) {
			baseHeaders['Authorization'] = `Bearer ${token}`;
		}
	}

	// Build final headers: Orval-provided headers take priority (they may set Content-Type)
	const finalHeaders = new Headers(baseHeaders);
	if (options?.headers) {
		const incoming = new Headers(options.headers);
		incoming.forEach((value, key) => finalHeaders.set(key, value));
	}

	const response = await fetch(url, {
		...options,
		headers: finalHeaders
	});

	// 204 No Content — return empty
	if (response.status === 204) {
		return undefined as T;
	}

	let data: unknown;
	const contentType = response.headers.get('content-type') ?? '';
	if (contentType.includes('application/json')) {
		data = await response.json();
	} else {
		data = await response.text();
	}

	if (!response.ok) {
		// Axios-compatible error shape for error handlers in pages
		throw {
			response: {
				data,
				status: response.status,
				statusText: response.statusText
			}
		};
	}

	return data as T;
};
