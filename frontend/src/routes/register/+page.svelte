<script lang="ts">
	import { createRegisterRegisterApiAuthRegisterPost } from '$lib/api/generated/endpoints';
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

	// ДОДАНО: імпорт перекладача
	import { _ } from 'svelte-i18n';

	let email = $state('');
	let name = $state('');
	let password = $state('');
	let errorMessage = $state('');

	// Mutation result is a reactive object in Svelte 5 / TanStack Query v5
	const registerMutation = createRegisterRegisterApiAuthRegisterPost();

	function handleRegister(event: Event) {
		event.preventDefault();
		errorMessage = '';

		registerMutation.mutate(
			{
				data: {
					email,
					password,
					name,
					is_active: true,
					is_superuser: false,
					is_verified: false
				}
			},
			{
				onSuccess: () => {
					window.location.href = resolve('/login');
				},
				onError: (err) => {
					const detail = (err as any)?.response?.data?.detail;
					if (Array.isArray(detail)) {
						errorMessage = detail.map((d: any) => d.msg).join(', ');
					} else {
						// ЗМІНЕНО: Використання перекладу для помилки за замовчуванням
						errorMessage = detail || $_('auth.errorRegisterDefault');
					}
				}
			}
		);
	}
</script>

<svelte:head>
	<title>{$_('auth.pageTitleRegister')}</title>
</svelte:head>

<div class="flex min-h-[80vh] items-center justify-center">
	<Card class="w-full max-w-md border-slate-200/60 bg-white/50 shadow-lg backdrop-blur-xl">
		<CardHeader class="space-y-1">
			<CardTitle class="text-center text-2xl font-bold">{$_('auth.registerTitle')}</CardTitle>
			<CardDescription class="text-center">{$_('auth.registerDesc')}</CardDescription>
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

			<form onsubmit={handleRegister} class="space-y-4">
				<div class="space-y-2">
					<Label for="name">{$_('auth.nameLabel')}</Label>
					<Input
						id="name"
						type="text"
						bind:value={name}
						required
						placeholder={$_('auth.namePlaceholder')}
					/>
				</div>

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
					<Input id="password" type="password" bind:value={password} required minlength={8} />
				</div>

				<Button
					type="submit"
					class="w-full bg-blue-600 hover:bg-blue-700"
					disabled={registerMutation.isPending}
				>
					{#if registerMutation.isPending}
						{$_('auth.registeringBtn')}
					{:else}
						{$_('auth.registerBtn')}
					{/if}
				</Button>
			</form>
		</CardContent>
		<CardFooter class="flex justify-center">
			<p class="text-sm text-slate-500">
				{$_('auth.alreadyHaveAccount')}
				<a
					href={resolve('/login')}
					class="font-medium text-blue-600 transition-colors hover:text-blue-700 hover:underline"
				>
					{$_('auth.loginLink')}
				</a>
			</p>
		</CardFooter>
	</Card>
</div>
