<script lang="ts">
	import { createGetUsersApiV1UsersGet } from '$lib/api/generated/endpoints';
	import * as Table from '$lib/components/ui/table';
	import { Badge } from '$lib/components/ui/badge';
	import {
		Card,
		CardContent,
		CardDescription,
		CardHeader,
		CardTitle
	} from '$lib/components/ui/card';
	import { Users, ShieldCheck, Mail } from '@lucide/svelte';
	import type { UserRead } from '$lib/api/generated/model';

	let usersQuery = createGetUsersApiV1UsersGet(() => ({ offset: 0, limit: 100 }));

	function getUsers(): UserRead[] {
		const d = usersQuery.data;
		if (!d) return [];
		// Якщо бекенд повертає масив напряму
		if (Array.isArray(d)) return d as UserRead[];

		// Якщо бекенд загортає масив у поле data
		if (typeof d === 'object' && d !== null && 'data' in d) {
			const safeData = (d as Record<string, unknown>).data;
			if (Array.isArray(safeData)) {
				return safeData as UserRead[];
			}
		}
		return [];
	}

	// Реактивна змінна з готовим списком користувачів
	let usersList = $derived(getUsers());
</script>

<svelte:head>
	<title>Панель адміністратора - Користувачі</title>
</svelte:head>

<div class="mx-auto max-w-6xl space-y-6">
	<div class="flex items-center justify-between">
		<h1 class="flex items-center gap-3 text-3xl font-bold tracking-tight text-slate-900">
			<Users class="h-8 w-8 text-blue-600" />
			Управління користувачами
		</h1>
	</div>

	<Card class="border-slate-200 shadow-sm">
		<CardHeader class="pb-4">
			<CardTitle>Усі користувачі</CardTitle>
			<CardDescription>Перегляд та управління обліковими записами на платформі.</CardDescription>
		</CardHeader>
		<CardContent>
			{#if usersQuery.isLoading}
				<div class="flex h-48 items-center justify-center">
					<div class="h-8 w-8 animate-spin rounded-full border-b-2 border-blue-600"></div>
				</div>
			{:else if usersQuery.isError}
				<div class="rounded-lg bg-red-50 py-10 text-center text-red-600">
					<p class="font-medium">Не вдалося завантажити користувачів</p>
					<p class="text-sm opacity-80">Перевірте права доступу (потрібен статус адміністратора)</p>
				</div>
			{:else}
				<div class="rounded-md border border-slate-200">
					<Table.Root>
						<Table.Header>
							<Table.Row class="bg-slate-50/50 hover:bg-slate-50/50">
								<Table.Head class="w-[80px]">ID</Table.Head>
								<Table.Head>Користувач</Table.Head>
								<Table.Head>Email</Table.Head>
								<Table.Head>Роль</Table.Head>
								<Table.Head>Статус</Table.Head>
								<Table.Head class="text-right">Адмін</Table.Head>
							</Table.Row>
						</Table.Header>
						<Table.Body>
							{#each usersList as user (user.id)}
								<Table.Row>
									<Table.Cell class="font-medium text-slate-500">#{user.id}</Table.Cell>
									<Table.Cell class="font-medium">{user.name || 'Не вказано'}</Table.Cell>
									<Table.Cell>
										<div class="flex items-center gap-2 text-slate-600">
											<Mail class="h-4 w-4 opacity-50" />
											{user.email}
										</div>
									</Table.Cell>
									<Table.Cell>
										<Badge variant="outline" class="capitalize">{user.role}</Badge>
									</Table.Cell>
									<Table.Cell>
										{#if user.is_active}
											<Badge class="border-0 bg-green-100 text-green-800 hover:bg-green-100">
												Активний
											</Badge>
										{:else}
											<Badge variant="secondary">Заблокований</Badge>
										{/if}
									</Table.Cell>
									<Table.Cell class="text-right">
										{#if user.is_superuser}
											<ShieldCheck class="inline-block h-5 w-5 text-blue-600" />
										{:else}
											<span class="text-slate-300">-</span>
										{/if}
									</Table.Cell>
								</Table.Row>
							{/each}

							{#if usersList.length === 0}
								<Table.Row>
									<Table.Cell colspan={6} class="h-24 text-center text-slate-500">
										Користувачів не знайдено
									</Table.Cell>
								</Table.Row>
							{/if}
						</Table.Body>
					</Table.Root>
				</div>
			{/if}
		</CardContent>
	</Card>
</div>
