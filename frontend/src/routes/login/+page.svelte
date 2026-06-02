<script lang="ts">
	import { createAuthJwtLoginApiAuthJwtLoginPost } from '$lib/api/generated/endpoints';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import {
		Card,
		CardContent,
		CardDescription,
		CardFooter,
		CardHeader,
		CardTitle
	} from '$lib/components/ui/card';
	import { AlertCircle } from '@lucide/svelte';
	import { resolve } from '$app/paths';

	// ДОДАНО: імпорт функції перекладу
	import { _ } from 'svelte-i18n';

	let email = $state('');
	let password = $state('');
	let errorMessage = $state('');

	const loginMutation = createAuthJwtLoginApiAuthJwtLoginPost();

	function handleLogin(event: Event) {
		event.preventDefault();
		errorMessage = '';

		loginMutation.mutate(
			{
				data: {
					username: email,
					password,
					grant_type: 'password',
					scope: '',
					client_id: '',
					client_secret: ''
				}
			},
			{
				onSuccess: (response) => {
					const token = (response as any)?.access_token ?? (response as any)?.data?.access_token;

					if (token) {
						localStorage.setItem('access_token', token);
					}
					window.location.href = resolve('/campaigns');
				},
				onError: (err) => {
					// ДОДАНО: використання перекладу для помилки
					errorMessage = (err as any)?.response?.data?.detail || $_('auth.errorDefault');
				}
			}
		);
	}
</script>

<svelte:head>
	<title>{$_('auth.pageTitleLogin')}</title>
</svelte:head>

<div class="flex min-h-[80vh] items-center justify-center">
	<Card class="w-full max-w-md border-slate-200/60 bg-white/50 shadow-lg backdrop-blur-xl">
		<CardHeader class="space-y-1">
			<CardTitle class="text-center text-2xl font-bold">{$_('auth.loginTitle')}</CardTitle>
			<CardDescription class="text-center">{$_('auth.loginDesc')}</CardDescription>
		</CardHeader>

		<CardContent>
			{#if errorMessage}
				<div
					class="mb-6 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50/80 p-3 text-sm text-red-700"
				>
					<AlertCircle class="h-4 w-4 shrink-0" />
					<span>{errorMessage}</span>
				</div>
			{/if}

			<form onsubmit={handleLogin} class="space-y-4">
				<div class="space-y-2">
					<Label for="email">{$_('auth.emailLabel')}</Label>
					<Input
						id="email"
						type="email"
						bind:value={email}
						required
						placeholder="name@example.com"
					/>
				</div>
				<div class="space-y-2">
					<Label for="password">{$_('auth.passwordLabel')}</Label>
					<Input id="password" type="password" bind:value={password} required />
				</div>

				<Button
					type="submit"
					class="w-full bg-blue-600 hover:bg-blue-700"
					disabled={loginMutation.isPending}
				>
					{#if loginMutation.isPending}
						{$_('auth.loggingInBtn')}
					{:else}
						{$_('auth.loginBtn')}
					{/if}
				</Button>
			</form>
		</CardContent>

		<CardFooter class="flex justify-center">
			<p class="text-sm text-slate-500">
				{$_('auth.noAccount')}
				<a
					href={resolve('/register')}
					class="font-medium text-blue-600 transition-colors hover:text-blue-700 hover:underline"
				>
					{$_('auth.registerLink')}
				</a>
			</p>
		</CardFooter>
	</Card>
</div>
