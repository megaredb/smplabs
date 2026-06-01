<script lang="ts">
    import {
        createGetMyCampaignsApiV1CampaignsMyGet,
        createGetMyTransactionsApiV1TransactionsMyGet
    } from '$lib/api/generated/endpoints';
    import type { CampaignResponse } from '$lib/api/generated/model/campaignResponse';
    import type { TransactionResponse } from '$lib/api/generated/model/transactionResponse';
    import { Button } from '$lib/components/ui/button';
    import { Input } from '$lib/components/ui/input';
    import {
        Card,
        CardContent,
        CardDescription,
        CardFooter,
        CardHeader,
        CardTitle
    } from '$lib/components/ui/card';
    import { Progress } from '$lib/components/ui/progress';
    import * as Table from '$lib/components/ui/table';
    import { Search, Activity, ArrowRight } from '@lucide/svelte';
    import { resolve } from '$app/paths';
    
    // ДОДАНО: імпорт перекладу
    import { _ } from 'svelte-i18n';

    let campaignSearch = $state('');
    let transactionSearch = $state('');
    let campaignsQuery = createGetMyCampaignsApiV1CampaignsMyGet();
    let transactionsQuery = createGetMyTransactionsApiV1TransactionsMyGet();

    function getCampaigns(): CampaignResponse[] {
        const d = campaignsQuery.data;
        if (!d) return [];
        if (Array.isArray(d)) return d;
        const wrapped = d as { data?: unknown };
        if (Array.isArray(wrapped.data)) {
            return wrapped.data as CampaignResponse[];
        }
        return [];
    }

    function getTransactions(): TransactionResponse[] {
        const d = transactionsQuery.data;
        if (!d) return [];
        if (Array.isArray(d)) return d;
        const wrapped = d as { data?: unknown };
        if (Array.isArray(wrapped.data)) {
            return wrapped.data as TransactionResponse[];
        }
        return [];
    }

    let campaigns = $derived(getCampaigns());
    let transactions = $derived(getTransactions());
    let campaignCount = $derived(campaigns.length);
    let totalRaised = $derived(
        campaigns.reduce((sum, campaign) => sum + (campaign.current_amount ?? 0), 0)
    );
    let activeCampaigns = $derived(
        campaigns.filter((campaign) => (campaign.current_amount ?? 0) < Number(campaign.target_amount)).length
    );
    let lastDonation = $derived(transactions[0]?.amount ?? 0);

    let filteredCampaigns = $derived(
        campaigns.filter((campaign) => {
            if (!campaignSearch) return true;
            const text = `${campaign.title} ${campaign.description ?? ''}`.toLowerCase();
            return text.includes(campaignSearch.toLowerCase());
        })
    );

    let filteredTransactions = $derived(
        transactions.filter((transaction) => {
            if (!transactionSearch) return true;
            const text = `${transaction.campaign_id} ${transaction.comment ?? ''}`.toLowerCase();
            return text.includes(transactionSearch.toLowerCase());
        })
    );

    function formatMoney(value: number) {
        return `${value.toLocaleString('uk-UA')} ₴`;
    }

    function formatDate(value: string) {
        return new Date(value).toLocaleDateString('uk-UA', {
            day: '2-digit',
            month: 'short',
            year: 'numeric'
        });
    }

    function progressValue(campaign: CampaignResponse) {
        return Math.min(100, Math.round(((campaign.current_amount ?? 0) / Number(campaign.target_amount)) * 100));
    }

    function campaignStatusKey(campaign: CampaignResponse) {
        return (campaign.current_amount ?? 0) >= Number(campaign.target_amount) 
            ? 'userStats.statusCompleted' 
            : 'userStats.statusActive';
    }
</script>

<svelte:head>
    <title>{$_('userStats.pageTitle')}</title>
</svelte:head>

<div class="mx-auto max-w-7xl space-y-6">
    <section class="rounded-3xl border border-slate-200 bg-white/90 p-6 shadow-sm">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div class="space-y-2">
                <p class="text-sm font-medium tracking-[0.2em] uppercase text-slate-500">
                    {$_('userStats.subtitle')}
                </p>
                <h1 class="text-3xl font-semibold tracking-tight text-slate-900">
                    {$_('userStats.heading')}
                </h1>
                <p class="max-w-2xl text-sm text-slate-600">
                    {$_('userStats.description')}
                </p>
            </div>
            <div class="flex flex-wrap gap-3">
                <Button variant="outline" href={resolve('/campaigns')}>{$_('userStats.allCampaignsBtn')}</Button>
                <Button href={resolve('/campaigns/create')}>{$_('userStats.createCampaignBtn')}</Button>
            </div>
        </div>
    </section>

    <section class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <Card class="border-slate-200 shadow-sm">
            <CardHeader>
                <CardTitle>{$_('userStats.statCampaignsTitle')}</CardTitle>
            </CardHeader>
            <CardContent>
                <p class="mt-4 text-3xl font-semibold text-slate-900">{campaignCount}</p>
                <CardDescription class="mt-2 text-slate-500">{$_('userStats.statCampaignsDesc')}</CardDescription>
            </CardContent>
        </Card>
        <Card class="border-slate-200 shadow-sm">
            <CardHeader>
                <CardTitle>{$_('userStats.statActiveTitle')}</CardTitle>
            </CardHeader>
            <CardContent>
                <p class="mt-4 text-3xl font-semibold text-slate-900">{activeCampaigns}</p>
                <CardDescription class="mt-2 text-slate-500">{$_('userStats.statActiveDesc')}</CardDescription>
            </CardContent>
        </Card>
        <Card class="border-slate-200 shadow-sm">
            <CardHeader>
                <CardTitle>{$_('userStats.statRaisedTitle')}</CardTitle>
            </CardHeader>
            <CardContent>
                <p class="mt-4 text-3xl font-semibold text-slate-900">
                    {formatMoney(totalRaised)}
                </p>
                <CardDescription class="mt-2 text-slate-500">{$_('userStats.statRaisedDesc')}</CardDescription>
            </CardContent>
        </Card>
        <Card class="border-slate-200 shadow-sm">
            <CardHeader>
                <CardTitle>{$_('userStats.statLastDonationTitle')}</CardTitle>
            </CardHeader>
            <CardContent>
                <p class="mt-4 text-3xl font-semibold text-slate-900">
                    {lastDonation ? formatMoney(lastDonation) : $_('userStats.noData')}
                </p>
                <CardDescription class="mt-2 text-slate-500">
                    {$_('userStats.statLastDonationDesc')}
                </CardDescription>
            </CardContent>
        </Card>
    </section>

    <section class="space-y-4">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
                <h2 class="text-2xl font-semibold text-slate-900">{$_('userStats.myCampaignsTitle')}</h2>
                <p class="text-sm text-slate-600">
                    {$_('userStats.myCampaignsDesc')}
                </p>
            </div>
            <div class="flex w-full max-w-md items-center gap-3">
                <div class="relative w-full">
                    <Search class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                    <Input bind:value={campaignSearch} placeholder={$_('userStats.searchCampaignPlaceholder')} class="pl-10" />
                </div>
            </div>
        </div>

        {#if campaignsQuery.isLoading}
            <div class="flex items-center justify-center rounded-3xl border border-slate-200 bg-white/80 p-12 shadow-sm">
                <div class="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"></div>
            </div>
        {:else if campaignsQuery.isError}
            <Card class="border-red-200 bg-red-50/50">
                <CardContent class="py-10 text-center text-red-600">
                    <p class="font-medium">{$_('userStats.campaignsLoadError')}</p>
                </CardContent>
            </Card>
        {:else if filteredCampaigns.length === 0}
            <Card class="border-slate-200 bg-slate-50">
                <CardContent class="py-10 text-center text-slate-600">
                    <p class="font-medium">{$_('userStats.campaignsNotFound')}</p>
                </CardContent>
            </Card>
        {:else}
            <div class="grid gap-4 lg:grid-cols-2">
                {#each filteredCampaigns as campaign (campaign.id)}
                    <Card class="overflow-hidden border-slate-200 shadow-sm">
                        <CardContent class="space-y-4">
                            <div class="flex items-center justify-between gap-3">
                                <div>
                                    <p class="text-sm font-medium tracking-[0.2em] uppercase text-slate-500">
                                        {$_(campaignStatusKey(campaign))}
                                    </p>
                                    <h3 class="mt-2 text-xl font-semibold text-slate-900">
                                        {campaign.title}
                                    </h3>
                                </div>
                                <div class="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">
                                    {progressValue(campaign)}%
                                </div>
                            </div>
                            <p class="text-sm leading-6 text-slate-600">
                                {campaign.description ?? $_('userStats.noDescription')}
                            </p>
                            <div class="space-y-3">
                                <div class="flex items-center justify-between text-sm text-slate-600">
                                    <span>{$_('userStats.raised')}</span>
                                    <span class="font-semibold text-slate-900">
                                        {formatMoney(campaign.current_amount ?? 0)}
                                    </span>
                                </div>
                                <div class="flex items-center justify-between text-sm text-slate-600">
                                    <span>{$_('userStats.target')}</span>
                                    <span class="font-semibold text-slate-900">
                                        {formatMoney(Number(campaign.target_amount))}
                                    </span>
                                </div>
                            </div>
                            <Progress value={progressValue(campaign)} max={100} />
                        </CardContent>
                        <CardFooter class="border-t border-slate-100 bg-slate-50 p-4">
                            <Button
                                variant="ghost"
                                size="sm"
                                href={resolve(`/campaigns/${campaign.id}`)}
                                class="gap-2"
                            >
                                <ArrowRight class="h-4 w-4" />
                                {$_('userStats.viewBtn')}
                            </Button>
                        </CardFooter>
                    </Card>
                {/each}
            </div>
        {/if}
    </section>

    <section class="space-y-4">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
                <h2 class="text-2xl font-semibold text-slate-900">{$_('userStats.transactionsTitle')}</h2>
                <p class="text-sm text-slate-600">{$_('userStats.transactionsDesc')}</p>
            </div>
            <div class="flex w-full max-w-md items-center gap-3">
                <div class="relative w-full">
                    <Search class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                    <Input
                        bind:value={transactionSearch}
                        placeholder={$_('userStats.searchTransactionPlaceholder')}
                        class="pl-10"
                    />
                </div>
            </div>
        </div>

        {#if transactionsQuery.isLoading}
            <div class="flex items-center justify-center rounded-3xl border border-slate-200 bg-white/80 p-12 shadow-sm">
                <div class="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"></div>
            </div>
        {:else if transactionsQuery.isError}
            <Card class="border-red-200 bg-red-50/50">
                <CardContent class="py-10 text-center text-red-600">
                    <p class="font-medium">{$_('userStats.transactionsLoadError')}</p>
                </CardContent>
            </Card>
        {:else}
            <Card class="border-slate-200 shadow-sm">
                <CardHeader class="border-b border-slate-100 pb-4">
                    <div class="flex items-center gap-2">
                        <Activity class="h-5 w-5 text-blue-600" />
                        <CardTitle>{$_('userStats.recentTransactions')}</CardTitle>
                    </div>
                </CardHeader>
                <CardContent class="overflow-x-auto p-0">
                    {#if filteredTransactions.length === 0}
                        <div class="p-6 text-center text-slate-600">{$_('userStats.transactionsEmpty')}</div>
                    {:else}
                        <Table.Root>
                            <Table.Header>
                                <Table.Row class="bg-slate-50/80">
                                    <Table.Head>{$_('userStats.thDate')}</Table.Head>
                                    <Table.Head>{$_('userStats.thCampaign')}</Table.Head>
                                    <Table.Head>{$_('userStats.thAmount')}</Table.Head>
                                    <Table.Head>{$_('userStats.thComment')}</Table.Head>
                                </Table.Row>
                            </Table.Header>
                            <Table.Body>
                                {#each filteredTransactions as transaction (transaction.id)}
                                    <Table.Row>
                                        <Table.Cell>{formatDate(transaction.created_at ?? '')}</Table.Cell>
                                        <Table.Cell>
                                            <a
                                                href={resolve(`/campaigns/${transaction.campaign_id}`)}
                                                class="font-medium text-blue-600 hover:underline"
                                            >
                                                {$_('userStats.campaignLink')}{transaction.campaign_id}
                                            </a>
                                        </Table.Cell>
                                        <Table.Cell class="font-semibold text-slate-900">
                                            {formatMoney(transaction.amount ?? 0)}
                                        </Table.Cell>
                                        <Table.Cell class="text-slate-600">
                                            {transaction.comment ?? '—'}
                                        </Table.Cell>
                                    </Table.Row>
                                {/each}
                            </Table.Body>
                        </Table.Root>
                    {/if}
                </CardContent>
            </Card>
        {/if}
    </section>
</div>