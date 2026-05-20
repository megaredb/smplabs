<script lang="ts">
	import { page } from '$app/stores';
	import {
		createGetCampaignApiV1CampaignsCampaignIdGet,
		createUpdateCampaignApiV1CampaignsCampaignIdPatch,
		createCreateTransactionApiV1TransactionsPost
	} from '$lib/api/generated/endpoints';
	import type { CampaignResponse } from '$lib/api/generated/model';
	import { Button } from '$lib/components/ui/button';
	import {
		Card,
		CardContent,
		CardDescription,
		CardHeader,
		CardTitle
	} from '$lib/components/ui/card';
	import { Progress } from '$lib/components/ui/progress';
	import { Badge } from '$lib/components/ui/badge';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import { ArrowLeft, Clock, Target, Edit, Calendar } from '@lucide/svelte';
	import { resolve } from '$app/paths';
	import { onMount } from 'svelte';

	let campaignId = $derived(Number($page.params.id));
	let currentUserId = $state<number | null>(null);

	onMount(() => {
		const token = localStorage.getItem('access_token');
		if (token) {
			try {
				const payload = JSON.parse(atob(token.split('.')[1]));
				currentUserId = parseInt(payload.sub);
			} catch {
				// ignore parse errors
			}
		}
	});

	const campaignQuery = $derived(createGetCampaignApiV1CampaignsCampaignIdGet(() => campaignId));

	const updateMutation = createUpdateCampaignApiV1CampaignsCampaignIdPatch();
	const donateMutation = createCreateTransactionApiV1TransactionsPost();

	function getCampaign(): CampaignResponse | null {
		const d = campaignQuery.data;
		if (!d) return null;
		return d as unknown as CampaignResponse;
	}

	let isEditDialogOpen = $state(false);
	let editTitle = $state('');
	let editDescription = $state('');
	let editTargetAmount = $state('');

	function openEditDialog() {
		const campaign = getCampaign();
		if (campaign) {
			editTitle = campaign.title || '';
			editDescription = campaign.description || '';
			editTargetAmount = String(campaign.target_amount || '');
			isEditDialogOpen = true;
		}
	}

	function handleEdit(event: Event) {
		event.preventDefault();
		updateMutation.mutate(
			{
				campaignId,
				data: {
					title: editTitle,
					description: editDescription,
					target_amount: Number(editTargetAmount)
				}
			},
			{
				onSuccess: () => {
					isEditDialogOpen = false;
					campaignQuery.refetch();
				}
			}
		);
	}

	let isDonateDialogOpen = $state(false);
	let donateAmount = $state('');
	let donateComment = $state('');

	function handleDonate(event: Event) {
		event.preventDefault();
		donateMutation.mutate(
			{
				data: {
					campaign_id: campaignId,
					amount: Number(donateAmount),
					donor_id: currentUserId,
					comment: donateComment
				}
			},
			{
				onSuccess: () => {
					isDonateDialogOpen = false;
					donateAmount = '';
					donateComment = '';
					campaignQuery.refetch();
				}
			}
		);
	}
</script>

<svelte:head>
	<title>RazomFund - Деталі збору</title>
</svelte:head>

<div class="mx-auto max-w-4xl space-y-6">
	<Button
		variant="ghost"
		href={resolve('/campaigns')}
		class="-ml-4 flex items-center gap-2 text-slate-500 transition-colors hover:text-slate-900"
	>
		<ArrowLeft class="h-4 w-4" />
		Назад до зборів
	</Button>

	{#if campaignQuery.isLoading}
		<div class="flex h-64 items-center justify-center">
			<div class="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"></div>
		</div>
	{:else if campaignQuery.isError}
		<Card class="border-red-200 bg-red-50/50">
			<CardContent class="py-10 text-center text-red-600">
				<p class="mb-2 text-lg font-medium">Помилка завантаження</p>
				<p class="text-sm opacity-80">Не вдалося знайти збір</p>
			</CardContent>
		</Card>
	{:else}
		{@const campaign = getCampaign()}
		{#if campaign}
			{@const targetAmount = Number(campaign.target_amount) || 0}
			{@const currentAmount = Number(campaign.current_amount) || 0}
			{@const progress = Math.min(Math.round((currentAmount / (targetAmount || 1)) * 100), 100)}

			<div class="grid gap-6 md:grid-cols-3">
				<div class="space-y-6 md:col-span-2">
					<Card
						class="relative overflow-hidden border-slate-200 bg-white/80 shadow-sm backdrop-blur-sm"
					>
						{#if currentUserId === campaign.organizer_id}
							<Button
								variant="outline"
								class="absolute top-4 right-4 z-10 bg-white/80 backdrop-blur-sm hover:bg-white"
								onclick={openEditDialog}
							>
								<Edit class="mr-2 h-4 w-4" />
								Редагувати
							</Button>
						{/if}

						<div
							class="flex h-64 w-full items-center justify-center bg-linear-to-br from-slate-100 to-slate-200"
						>
							<span class="text-lg font-medium text-slate-400">Немає зображення</span>
						</div>
						<CardHeader>
							<div class="mb-2">
								<Badge class="bg-green-100 text-green-800 hover:bg-green-100">Активний</Badge>
							</div>
							<CardTitle class="text-3xl leading-tight font-bold text-slate-900"
								>{campaign.title}</CardTitle
							>
							<CardDescription
								class="pt-4 text-base leading-relaxed whitespace-pre-wrap text-slate-700"
							>
								{campaign.description}
							</CardDescription>
						</CardHeader>
					</Card>
				</div>

				<div class="space-y-6">
					<Card class="sticky top-24 border-slate-200 bg-white shadow-sm">
						<CardHeader class="border-b border-slate-50 pb-4">
							<CardTitle class="text-xl">Статус збору</CardTitle>
						</CardHeader>
						<CardContent class="space-y-6 pt-6">
							<div class="space-y-2">
								<div class="flex items-end justify-between text-sm">
									<span class="text-3xl font-bold text-slate-900">{currentAmount} ₴</span>
									<span class="mb-1 text-slate-500">з {targetAmount} ₴</span>
								</div>
								<Progress value={progress} class="h-3 bg-slate-100 [&>div]:bg-blue-600" />
							</div>

							<div class="grid grid-cols-3 gap-4 border-t border-slate-100 pt-4">
								<div class="space-y-1">
									<div class="flex items-center gap-1.5 text-xs text-slate-500">
										<Target class="h-4 w-4" />
										<span>Прогрес</span>
									</div>
									<p class="text-sm font-semibold text-slate-900">{progress}%</p>
								</div>
								<div class="space-y-1">
									<div class="flex items-center gap-1.5 text-xs text-slate-500">
										<Clock class="h-4 w-4" />
										<span>Створено</span>
									</div>
									<p class="text-[11px] font-semibold text-slate-900">
										{campaign.created_at
											? new Date(campaign.created_at).toLocaleDateString('uk-UA')
											: '—'}
									</p>
								</div>
								<div class="space-y-1">
									<div class="flex items-center gap-1.5 text-xs text-slate-500">
										<Calendar class="h-4 w-4" />
										<span>Кінець</span>
									</div>
									<p class="text-[11px] font-semibold text-blue-600">
										{campaign.created_at
											? new Date(
													new Date(campaign.created_at).getTime() + 14 * 24 * 60 * 60 * 1000
												).toLocaleDateString('uk-UA')
											: '—'}
									</p>
								</div>
							</div>

							<Button
								size="lg"
								class="w-full bg-blue-600 py-6 text-base font-semibold shadow-md transition-all hover:bg-blue-700 active:scale-[0.98]"
								onclick={() => (isDonateDialogOpen = true)}
							>
								Підтримати збір
							</Button>
						</CardContent>
					</Card>
				</div>
			</div>

			<Dialog.Root bind:open={isEditDialogOpen}>
				<Dialog.Content class="sm:max-w-[500px]">
					<Dialog.Header>
						<Dialog.Title>Редагування збору</Dialog.Title>
						<Dialog.Description>Оновіть інформацію про ваш збір.</Dialog.Description>
					</Dialog.Header>
					<form onsubmit={handleEdit} class="space-y-4 py-4">
						<div class="space-y-2">
							<Label for="edit-title">Назва</Label>
							<Input id="edit-title" bind:value={editTitle} required />
						</div>
						<div class="space-y-2">
							<Label for="edit-desc">Опис</Label>
							<Textarea id="edit-desc" bind:value={editDescription} rows={4} />
						</div>
						<div class="space-y-2">
							<Label for="edit-target">Ціль (₴)</Label>
							<Input
								id="edit-target"
								type="number"
								min="1"
								bind:value={editTargetAmount}
								required
							/>
						</div>
						<Dialog.Footer>
							<Button type="button" variant="outline" onclick={() => (isEditDialogOpen = false)}
								>Скасувати</Button
							>
							<Button type="submit" disabled={updateMutation.isPending}>Зберегти зміни</Button>
						</Dialog.Footer>
					</form>
				</Dialog.Content>
			</Dialog.Root>

			<Dialog.Root bind:open={isDonateDialogOpen}>
				<Dialog.Content class="sm:max-w-[425px]">
					<Dialog.Header>
						<Dialog.Title>Зробити внесок</Dialog.Title>
						<Dialog.Description>Підтримайте цей збір будь-якою сумою.</Dialog.Description>
					</Dialog.Header>
					<form onsubmit={handleDonate} class="space-y-4 py-4">
						<div class="space-y-2">
							<Label for="donate-amount">Сума (₴)</Label>
							<Input
								id="donate-amount"
								type="number"
								min="1"
								bind:value={donateAmount}
								required
								placeholder="500"
							/>
						</div>
						<div class="space-y-2">
							<Label for="donate-comment">Коментар (необов'язково)</Label>
							<Textarea
								id="donate-comment"
								bind:value={donateComment}
								placeholder="Слава Україні!"
								rows={3}
							/>
						</div>
						<Dialog.Footer>
							<Button type="button" variant="outline" onclick={() => (isDonateDialogOpen = false)}
								>Скасувати</Button
							>
							<Button
								type="submit"
								class="bg-blue-600 hover:bg-blue-700"
								disabled={donateMutation.isPending}>Поповнити</Button
							>
						</Dialog.Footer>
					</form>
				</Dialog.Content>
			</Dialog.Root>
		{/if}
	{/if}
</div>
