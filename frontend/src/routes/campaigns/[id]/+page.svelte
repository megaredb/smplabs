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
    import { ArrowLeft, Clock, Target, Edit, Calendar, Plus, User, AlertTriangle, BadgeCheck } from '@lucide/svelte';
    import { resolve } from '$app/paths';
    import { onMount } from 'svelte';
    import { get } from 'svelte/store'; // Для використання в алертах

    // ДОДАНО: імпорт перекладу
    import { _ } from 'svelte-i18n';

    import { 
        createGetReportsApiV1CampaignsCampaignIdReportsGet, 
        createCreateReportApiV1CampaignsCampaignIdReportsPost 
    } from '$lib/api/generated/endpoints';

    import { createCreateComplaintApiV1CampaignsCampaignIdComplaintsPost } from '$lib/api/generated/endpoints';

    let isReportCampaignOpen = $state(false);
    let reportReason = $state('');
    const complaintMutation = createCreateComplaintApiV1CampaignsCampaignIdComplaintsPost();

    let campaignId = $derived(Number($page.params.id));
    let currentUserId = $state<number | null>(null);
    let myUid = $state('');
    let messages = $state<string[]>([]);
    let newMessage = $state('');
    let targetUser = $state('');
    let ws = $state<WebSocket | null>(null);

    function sendMessage() {
        if (!targetUser.trim()) {
            alert(get(_)('campaignDetails.enterRecipientAlert'));
            return;
        }
        if (ws && newMessage.trim() !== '') {
            ws.send(`${targetUser}:${newMessage}`);
            newMessage = '';
        }
    }

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
        const cid = campaignId;
        const uid = currentUserId
            ? `User_${currentUserId}`
            : `Guest_${Math.floor(Math.random() * 1000)}`;
        myUid = uid;
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        ws = new WebSocket(`${protocol}//${window.location.host}/ws/chat/${cid}/${uid}`);
        ws.onmessage = (event) => {
            messages = [...messages, event.data];
        };
        return () => {
            if (ws) ws.close();
        };
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
	let editEndDate = $state(''); // НОВЕ
    let editImageUrl = $state(''); // НОВЕ
    let editCategory = $state(''); // НОВЕ

    const categoryOptions = [
        { id: "ЗСУ / Військові", key: 'categories.military' },
        { id: "Медицина", key: 'categories.medical' },
        { id: "Відбудова", key: 'categories.rebuild' },
        { id: "Тварини", key: 'categories.animals' },
        { id: "Інше", key: 'categories.other' }
    ];

    function translateCategory(cat: string) {
        const match = categoryOptions.find(c => c.id === cat);
        return match ? $_(match.key) : (cat || $_('categories.other'));
    }

    function openEditDialog() {
        const campaign = getCampaign();
        if (campaign) {
            editTitle = campaign.title || '';
            editDescription = campaign.description || '';
            editTargetAmount = String(campaign.target_amount || '');
            // Витягуємо дату формату YYYY-MM-DD для інпуту
            editEndDate = (campaign as any).end_date ? new Date((campaign as any).end_date).toISOString().split('T')[0] : '';
            editImageUrl = (campaign as any).image_url || '';
            editCategory = (campaign as any).category || 'Інше';
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
                    target_amount: Number(editTargetAmount),
                    end_date: editEndDate ? new Date(editEndDate).toISOString() : null, // НОВЕ
                    image_url: editImageUrl || null, // НОВЕ
                    category: editCategory // НОВЕ
                } as any
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

		const campaign = getCampaign();
        if (campaign) {
            const maxAllowed = Number(campaign.target_amount) - Number(campaign.current_amount);
            if (Number(donateAmount) > maxAllowed) {
                alert(`Максимальна сума донату: ${maxAllowed} ₴`);
                return;
            }
        }

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

    let activeTab = $state('description'); // 'description' або 'reports'
    
    let isReportDialogOpen = $state(false);
    let reportTitle = $state('');
    let reportDescription = $state('');
    let reportImageUrl = $state('');

    // СТАЛО: другий аргумент тепер теж є стрілочною функцією
    const reportsQuery = $derived(
        createGetReportsApiV1CampaignsCampaignIdReportsGet(
            () => campaignId, 
            () => ({ query: { enabled: !!campaignId } } as any) // <-- ДОДАНО () =>
        )
    );

    const reportMutation = createCreateReportApiV1CampaignsCampaignIdReportsPost();

    function handleCreateReport(event: Event) {
        event.preventDefault();
        reportMutation.mutate(
            {
                campaignId,
                data: {
                    title: reportTitle,
                    description: reportDescription,
                    image_url: reportImageUrl || null
                } as any
            },
            {
                onSuccess: () => {
                    isReportDialogOpen = false;
                    reportTitle = '';
                    reportDescription = '';
                    reportImageUrl = '';
                    reportsQuery.refetch(); // Оновлюємо список звітів
                }
            }
        );
    }

    function handleComplaint(event: Event) {
        event.preventDefault();
        complaintMutation.mutate({
            campaignId,
            data: { reason: reportReason } as any
        }, {
            onSuccess: () => {
                isReportCampaignOpen = false;
                reportReason = '';
                alert("Скаргу успішно відправлено модераторам!");
            }
        });
    }
</script>

<svelte:head>
    <title>{$_('campaignDetails.pageTitle')}</title>
</svelte:head>

<div class="mx-auto max-w-4xl space-y-6">
    <Button
        variant="ghost"
        href={resolve('/campaigns')}
        class="-ml-4 flex items-center gap-2 text-slate-500 transition-colors hover:text-slate-900"
    >
        <ArrowLeft class="h-4 w-4" />
        {$_('campaignDetails.backBtn')}
    </Button>
    {#if campaignQuery.isLoading}
        <div class="flex h-64 items-center justify-center">
            <div class="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"></div>
        </div>
    {:else if campaignQuery.isError}
        <Card class="border-red-200 bg-red-50/50">
            <CardContent class="py-10 text-center text-red-600">
                <p class="mb-2 text-lg font-medium">{$_('campaignDetails.loadError')}</p>
                <p class="text-sm opacity-80">{$_('campaignDetails.notFound')}</p>
            </CardContent>
        </Card>
    {:else}
        {@const campaign = getCampaign()}
        {#if campaign}
            {@const targetAmount = Number(campaign.target_amount) || 0}
            {@const currentAmount = Number(campaign.current_amount) || 0}
            {@const progress = Math.min(Math.round((currentAmount / (targetAmount || 1)) * 100), 100)}
			{@const remainingAmount = Math.max(targetAmount - currentAmount, 0)}
            {@const isClosed = (campaign as any).end_date ? new Date((campaign as any).end_date) < new Date() : false}
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
                                {$_('campaignDetails.editBtn')}
                            </Button>
                        {/if}

                        {#if (campaign as any).image_url}
                            <img src={(campaign as any).image_url} alt={campaign.title} class="h-64 w-full object-cover" />
                        {:else}
                            <div
                                class="flex h-64 w-full items-center justify-center bg-linear-to-br from-slate-100 to-slate-200"
                            >
                                <span class="text-lg font-medium text-slate-400">{$_('campaignDetails.noImage')}</span>
                            </div>
                        {/if}
                        <CardHeader>
                            <div class="mb-2 flex items-center justify-between">
                                <div class="flex items-center gap-2">
                                    {#if (campaign as any).status === 'active'}
                                        <Badge class="bg-green-100 text-green-800 hover:bg-green-100">{$_('campaignDetails.statusActive')}</Badge>
                                    {:else if (campaign as any).status === 'pending'}
                                        <Badge class="bg-yellow-100 text-yellow-800 hover:bg-yellow-100">{$_('campaignDetails.statusPending')}</Badge>
                                    {:else}
                                        <Badge class="bg-slate-100 text-slate-800">{(campaign as any).status}</Badge>
                                    {/if}
                                    <Badge variant="outline" class="text-slate-600">{translateCategory((campaign as any).category)}</Badge>
                                </div>
                                
                                {#if currentUserId && currentUserId !== campaign.organizer_id}
                                    <button onclick={() => isReportCampaignOpen = true} class="text-sm flex items-center gap-1 text-slate-400 hover:text-red-500 transition-colors">
                                        <AlertTriangle class="h-4 w-4" />
                                        {$_('campaignDetails.reportBtn')}
                                    </button>
                                {/if}
                            </div>
                            <CardTitle class="text-3xl leading-tight font-bold text-slate-900">
                                {campaign.title}
                            </CardTitle>
                            
                            <div class="mt-4 flex items-center gap-2 text-slate-600 border-t border-slate-100 pt-4">
                                <div class="flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 relative">
                                    <User class="h-4 w-4 text-slate-500" />
                                    {#if (campaign as any).is_verified}
                                        <div class="absolute -bottom-1 -right-1 rounded-full bg-white">
                                            <BadgeCheck class="h-4 w-4 text-blue-500" />
                                        </div>
                                    {/if}
                                </div>
                                <span class="text-sm flex items-center gap-2">
                                    {$_('campaignDetails.organizerLabel')}: 
                                    <strong class="font-medium text-slate-900">
                                        {(campaign as any).organizer_name || $_('campaignDetails.defaultOrganizer')}
                                    </strong>
                                    {#if (campaign as any).is_verified}
                                        <span class="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full">{$_('campaignDetails.verified')}</span>
                                    {/if}
                                </span>
                            </div>
                        </CardHeader>
                        <div class="border-b border-slate-200 px-6 mt-4">
                            <nav class="-mb-px flex space-x-8" aria-label="Tabs">
                                <button
                                    type="button"
                                    onclick={() => activeTab = 'description'}
                                    class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors {activeTab === 'description' ? 'border-blue-500 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'}"
                                >
                                    {$_('campaignDetails.tabDescription')}
                                </button>
                                <button
                                    type="button"
                                    onclick={() => activeTab = 'reports'}
                                    class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors {activeTab === 'reports' ? 'border-blue-500 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'}"
                                >
                                    {$_('campaignDetails.tabReports')}
                                </button>
                            </nav>
                        </div>

                        <div class="px-6 pb-6 pt-6">
                            {#if activeTab === 'description'}
                                <div class="text-base leading-relaxed whitespace-pre-wrap text-slate-700">
                                    {campaign.description}
                                </div>
                            {:else if activeTab === 'reports'}
                                <div class="space-y-6">
                                    <div class="flex justify-between items-center">
                                        <h3 class="text-lg font-semibold text-slate-900">{$_('campaignDetails.reportsTitle')}</h3>
                                        {#if currentUserId === campaign.organizer_id}
                                            <Button variant="outline" size="sm" onclick={() => isReportDialogOpen = true}>
                                                <Plus class="mr-2 h-4 w-4" />
                                                {$_('campaignDetails.addReportBtn')}
                                            </Button>
                                        {/if}
                                    </div>
                                    
                                    {#if reportsQuery.data && reportsQuery.data.length > 0}
                                        <div class="space-y-6 mt-4">
                                            {#each reportsQuery.data as report}
                                                <Card class="overflow-hidden border border-slate-200 shadow-sm">
                                                    {#if report.image_url}
                                                        <img src={report.image_url} alt={report.title} class="h-64 w-full object-cover" />
                                                    {/if}
                                                    <CardHeader class="p-5 pb-2">
                                                        <CardTitle class="text-xl font-bold">{report.title}</CardTitle>
                                                        <div class="text-sm text-slate-500 mt-1">
                                                            {new Date(report.created_at).toLocaleDateString('uk-UA', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute:'2-digit' })}
                                                        </div>
                                                    </CardHeader>
                                                    <CardContent class="p-5 pt-2 text-slate-700 whitespace-pre-wrap">
                                                        {report.description}
                                                    </CardContent>
                                                </Card>
                                            {/each}
                                        </div>
                                    {:else}
                                        <div class="py-10 text-center text-slate-500 bg-slate-50 rounded-lg border border-dashed border-slate-300">
                                            {$_('campaignDetails.noReports')}
                                        </div>
                                    {/if}
                                </div>
                            {/if}
                        </div>
                    </Card>
                </div>
                <div class="space-y-6">
                    <Card class="sticky top-24 border-slate-200 bg-white shadow-sm">
                        <CardHeader class="border-b border-slate-50 pb-4">
                            <CardTitle class="text-xl">{$_('campaignDetails.statusTitle')}</CardTitle>
                        </CardHeader>
                        <CardContent class="space-y-6 pt-6">
                            <div class="space-y-2">
                                <div class="flex items-end justify-between text-sm">
                                    <span class="text-3xl font-bold text-slate-900">{currentAmount} ₴</span>
                                    <span class="mb-1 text-slate-500">{$_('campaignDetails.of')} {targetAmount} ₴</span>
                                </div>
                                <Progress value={progress} class="h-3 bg-slate-100 [&>div]:bg-blue-600" />
                            </div>
                            <div class="grid grid-cols-3 gap-4 border-t border-slate-100 pt-4">
                                <div class="space-y-1">
                                    <div class="flex items-center gap-1.5 text-xs text-slate-500">
                                        <Target class="h-4 w-4" />
                                        <span>{$_('campaignDetails.progress')}</span>
                                    </div>
                                    <p class="text-sm font-semibold text-slate-900">{progress}%</p>
                                </div>
                                <div class="space-y-1">
                                    <div class="flex items-center gap-1.5 text-xs text-slate-500">
                                        <Clock class="h-4 w-4" />
                                        <span>{$_('campaignDetails.created')}</span>
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
                                        <span>{$_('campaignDetails.ends')}</span>
                                    </div>
                                    <p class="text-[11px] font-semibold text-blue-600">
                                        {(campaign as any).end_date
                                            ? new Date((campaign as any).end_date).toLocaleDateString('uk-UA')
                                            : '—'}
                                    </p>
                                </div>
                            </div>
                            <Button
                                size="lg"
                                class="w-full py-6 text-base font-semibold shadow-md transition-all active:scale-[0.98] {isClosed || remainingAmount <= 0 ? 'bg-slate-300 text-slate-500 hover:bg-slate-300 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}"
                                onclick={() => (isDonateDialogOpen = true)}
                                disabled={isClosed || remainingAmount <= 0}
                            >
                                {#if remainingAmount <= 0}
                                    {$_('campaignDetails.statusFullyFunded')}
                                {:else if isClosed}
                                    {$_('campaignDetails.statusClosed')}
                                {:else}
                                    {$_('campaignDetails.supportBtn')}
                                {/if}
                            </Button>
                        </CardContent>
                    </Card>
                </div>
            </div>

            <Dialog.Root bind:open={isEditDialogOpen}>
                <Dialog.Content class="bg-white sm:max-w-[500px]">
                    <Dialog.Header>
                        <Dialog.Title>{$_('campaignDetails.editDialogTitle')}</Dialog.Title>
                        <Dialog.Description>{$_('campaignDetails.editDialogDesc')}</Dialog.Description>
                    </Dialog.Header>
                    <form onsubmit={handleEdit} class="space-y-4 py-4">
                        <div class="space-y-2">
                            <Label for="edit-title">{$_('campaignDetails.titleLabel')}</Label>
                            <Input id="edit-title" bind:value={editTitle} required />
                        </div>
                        <div class="space-y-2">
                            <Label for="edit-desc">{$_('campaignDetails.descLabel')}</Label>
                            <Textarea id="edit-desc" bind:value={editDescription} rows={4} />
                        </div>
                        <div class="space-y-2">
                            <Label for="edit-target">{$_('campaignDetails.targetLabel')}</Label>
                            <Input
                                id="edit-target"
                                type="number"
                                min="1"
                                bind:value={editTargetAmount}
                                required
                            />
                        </div>
						<div class="grid grid-cols-2 gap-4">
                            <div class="space-y-2">
                                <Label for="edit-target">{$_('campaignDetails.targetLabel')}</Label>
                                <Input id="edit-target" type="number" min="1" bind:value={editTargetAmount} required />
                            </div>
                            <div class="space-y-2">
                                <Label for="edit-end-date">{$_('campaignDetails.endDateLabel')}</Label>
                                <Input id="edit-end-date" type="date" bind:value={editEndDate} />
                            </div>
                        </div>
                        <div class="space-y-2">
                            <Label for="edit-category">{$_('categories.label')}</Label>
                            <select id="edit-category" bind:value={editCategory} class="flex h-10 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                                {#each categoryOptions as cat}
                                    <option value={cat.id}>{$_(cat.key)}</option>
                                {/each}
                            </select>
                        </div>
                        <div class="space-y-2">
                            <Label for="edit-image">{$_('campaignDetails.imageUrlLabel')}</Label>
                            <Input id="edit-image" type="url" bind:value={editImageUrl} />
                        </div>
                        <Dialog.Footer>
                            <Button type="button" variant="outline" onclick={() => (isEditDialogOpen = false)}
                                >{$_('campaignDetails.cancelBtn')}</Button
                            >
                            <Button type="submit" disabled={updateMutation.isPending}>{$_('campaignDetails.saveBtn')}</Button>
                        </Dialog.Footer>
                    </form>
                </Dialog.Content>
            </Dialog.Root>

            <Dialog.Root bind:open={isDonateDialogOpen}>
                <Dialog.Content class="bg-white sm:max-w-[425px]">
                    <Dialog.Header>
                        <Dialog.Title>{$_('campaignDetails.donateDialogTitle')}</Dialog.Title>
                        <Dialog.Description>{$_('campaignDetails.donateDialogDesc')}</Dialog.Description>
                    </Dialog.Header>
                    <form onsubmit={handleDonate} class="space-y-4 py-4">
                        <div class="space-y-2">
                            <Label for="donate-amount">{$_('campaignDetails.amountLabel')}</Label>
                            <Input
                                id="donate-amount"
                                type="number"
                                min="1"
                                max={remainingAmount}
                                bind:value={donateAmount}
                                required
                                placeholder="500"
                            />
                        </div>
                        <div class="space-y-2">
                            <Label for="donate-comment">{$_('campaignDetails.commentLabel')}</Label>
                            <Textarea
                                id="donate-comment"
                                bind:value={donateComment}
                                placeholder={$_('campaignDetails.commentPlaceholder')}
                                rows={3}
                            />
                        </div>
                        <Dialog.Footer>
                            <Button type="button" variant="outline" onclick={() => (isDonateDialogOpen = false)}
                                >{$_('campaignDetails.cancelBtn')}</Button
                            >
                            <Button
                                type="submit"
                                class="bg-blue-600 hover:bg-blue-700"
                                disabled={donateMutation.isPending}>{$_('campaignDetails.donateBtn')}</Button
                            >
                        </Dialog.Footer>
                    </form>
                </Dialog.Content>
            </Dialog.Root>

            <Dialog.Root bind:open={isReportDialogOpen}>
                <Dialog.Content class="bg-white sm:max-w-[550px]">
                    <Dialog.Header>
                        <Dialog.Title>{$_('campaignDetails.addReportBtn')}</Dialog.Title>
                    </Dialog.Header>
                    <form onsubmit={handleCreateReport} class="space-y-4 py-4">
                        <div class="space-y-2">
                            <Label for="report-title">{$_('campaignDetails.reportTitleLabel')}</Label>
                            <Input id="report-title" bind:value={reportTitle} required />
                        </div>
                        <div class="space-y-2">
                            <Label for="report-desc">{$_('campaignDetails.reportDescLabel')}</Label>
                            <textarea 
                                id="report-desc" 
                                bind:value={reportDescription} 
                                required 
                                rows="5" 
                                class="w-full resize-y rounded-md border border-slate-300 bg-transparent px-3 py-2 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2"
                            ></textarea>
                        </div>
                        <div class="space-y-2">
                            <Label for="report-image">{$_('campaignDetails.reportImageLabel')}</Label>
                            <Input id="report-image" type="url" bind:value={reportImageUrl} />
                        </div>
                        <Dialog.Footer class="pt-4">
                            <Button type="button" variant="outline" onclick={() => isReportDialogOpen = false}>{$_('campaignDetails.cancelBtn')}</Button>
                            <Button type="submit" class="bg-blue-600 hover:bg-blue-700" disabled={reportMutation.isPending}>
                                {$_('campaignDetails.reportSubmitBtn')}
                            </Button>
                        </Dialog.Footer>
                    </form>
                </Dialog.Content>
            </Dialog.Root>
        {/if}

        <!-- UI Чату (Лабораторна) -->
        <div class="mt-12 max-w-md rounded-lg border bg-white p-4 shadow-sm">
            <h3 class="mb-2 border-b pb-2 text-lg font-semibold text-gray-800">{$_('campaignDetails.chatTitle')}</h3>
            <p class="mb-4 text-xs text-gray-500">{$_('campaignDetails.yourId')} <strong>{myUid}</strong></p>
            <div
                class="mb-4 flex h-64 flex-col gap-2 overflow-y-auto rounded border bg-gray-50 p-3 text-sm"
            >
                {#each messages as msg}
                    <div class="rounded border bg-white p-2 break-words text-gray-700 shadow-sm">
                        {msg}
                    </div>
                {/each}
                {#if messages.length === 0}
                    <div class="mt-10 text-center text-gray-400 italic">{$_('campaignDetails.noMessages')}</div>
                {/if}
            </div>
            <div class="mb-2">
                <input
                    type="text"
                    bind:value={targetUser}
                    placeholder={$_('campaignDetails.toPlaceholder')}
                    class="w-full rounded border px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
            </div>
            <div class="flex gap-2">
                <input
                    type="text"
                    bind:value={newMessage}
                    onkeydown={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder={$_('campaignDetails.msgPlaceholder')}
                    class="flex-1 rounded border px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
                <button
                    onclick={sendMessage}
                    class="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
                >
                    {$_('campaignDetails.sendBtn')}
                </button>
            </div>
        </div>
    {/if}
    <Dialog.Root bind:open={isReportCampaignOpen}>
        <Dialog.Content class="bg-white sm:max-w-[425px]">
            <Dialog.Header>
                <Dialog.Title class="text-red-600 flex items-center gap-2">
                    <AlertTriangle class="h-5 w-5" />
                    {$_('campaignDetails.reportDialogTitle')}
                </Dialog.Title>
            </Dialog.Header>
            <form onsubmit={handleComplaint} class="space-y-4 py-4">
                <div class="space-y-2">
                    <Label for="complaint-reason">{$_('campaignDetails.reportReasonLabel')}</Label>
                    <textarea 
                        id="complaint-reason" 
                        bind:value={reportReason} 
                        required 
                        rows="4" 
                        class="w-full resize-y rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-500"
                    ></textarea>
                </div>
                <Dialog.Footer>
                    <Button type="button" variant="outline" onclick={() => isReportCampaignOpen = false}>{$_('campaignDetails.cancelBtn')}</Button>
                    <Button type="submit" class="bg-red-600 hover:bg-red-700" disabled={complaintMutation.isPending}>
                        {$_('campaignDetails.reportSubmitBtn')}
                    </Button>
                </Dialog.Footer>
            </form>
        </Dialog.Content>
    </Dialog.Root>
</div>