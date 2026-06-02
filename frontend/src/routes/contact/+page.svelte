<script lang="ts">
	import { _ } from 'svelte-i18n';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { MailCheck } from '@lucide/svelte';

	let isSubmitted = $state(false);

	function handleSubmit(event: Event) {
		event.preventDefault();
		// В реальному проекті тут був би API-запит
		isSubmitted = true;
	}
</script>

<svelte:head>
	<title>{$_('contact.title')} | RazomFund</title>
</svelte:head>

<div class="mx-auto max-w-2xl px-4 py-12 sm:px-6">
	<div class="mb-10 text-center">
		<h1 class="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
			{$_('contact.title')}
		</h1>
		<p class="mt-4 text-lg text-slate-600">{$_('contact.desc')}</p>
	</div>

	{#if isSubmitted}
		<div
			class="flex flex-col items-center justify-center rounded-xl border border-green-200 bg-green-50 p-8 text-center text-green-800"
		>
			<MailCheck class="mb-4 h-12 w-12 text-green-600" />
			<p class="text-lg font-medium">{$_('contact.successMsg')}</p>
		</div>
	{:else}
		<form
			onsubmit={handleSubmit}
			class="space-y-6 rounded-xl border border-slate-200 bg-white p-8 shadow-sm"
		>
			<div class="space-y-2">
				<Label for="name">{$_('contact.nameLabel')}</Label>
				<Input id="name" required />
			</div>

			<div class="space-y-2">
				<Label for="email">{$_('contact.emailLabel')}</Label>
				<Input id="email" type="email" required />
			</div>

			<div class="space-y-2">
				<Label for="message">{$_('contact.msgLabel')}</Label>
				<textarea
					id="message"
					required
					rows="5"
					class="w-full resize-y rounded-md border border-slate-300 bg-transparent px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none"
				></textarea>
			</div>

			<Button type="submit" class="w-full bg-blue-600 hover:bg-blue-700">
				{$_('contact.submitBtn')}
			</Button>
		</form>
	{/if}
</div>
