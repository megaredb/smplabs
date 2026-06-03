<script lang="ts">
	import { onMount } from 'svelte';
	import { testXmlParsingApiLabXmlTestGet } from '$lib/api/generated/endpoints';

	let campaigns: any[] = $state([]);
	let loading = $state(true);
	let error = $state('');

	onMount(async () => {
		try {
			// Виклик API через згенеровану функцію Orval
			const response = await testXmlParsingApiLabXmlTestGet();

			// Нормалізація даних
			const rawData = response as any;
			let items = rawData?.data?.campaign || rawData?.data?.user;

			if (items) {
				// Якщо це один об'єкт, робимо з нього масив
				campaigns = Array.isArray(items) ? items : [items];
			} else {
				campaigns = [];
			}
		} catch (err) {
			console.error(err);
			error = 'Помилка при завантаженні або парсингу XML';
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>Лабораторна №4: XML Парсер</title>
</svelte:head>

<div class="mx-auto max-w-4xl p-6">
	<h1 class="mb-6 text-2xl font-bold text-gray-900">Лабораторна №4: XML Парсер</h1>

	{#if loading}
		<div class="animate-pulse text-gray-500">Завантаження...</div>
	{:else if error}
		<div class="font-medium text-red-500">{error}</div>
	{:else if campaigns.length === 0}
		<div class="text-gray-500">XML файл порожній</div>
	{:else}
		<div class="overflow-x-auto rounded-lg border border-gray-200 shadow-sm">
			<table class="min-w-full divide-y divide-gray-300 bg-white text-sm">
				<thead class="bg-gray-50">
					<tr>
						<th class="w-1/4 px-4 py-3 text-left font-semibold text-gray-900"
							>Тип збору (Атрибути)</th
						>
						<th class="w-3/4 px-4 py-3 text-left font-semibold text-gray-900">Вміст</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200">
					{#each campaigns as item}
						<tr>
							<td class="px-4 py-3 align-top font-medium text-gray-700">
								{#if item._attributes}
									<div class="flex flex-col gap-1">
										{#each Object.entries(item._attributes) as [key, val]}
											<span
												class="inline-flex rounded-full bg-blue-50 px-2 py-1 text-xs font-semibold text-blue-700"
											>
												{key}: {val}
											</span>
										{/each}
									</div>
								{:else}
									<span class="text-gray-400 italic">Немає атрибутів</span>
								{/if}
							</td>
							<td class="px-4 py-3 text-gray-600">
								<pre
									class="rounded border border-gray-100 bg-gray-50 p-3 font-mono text-xs whitespace-pre-wrap">{JSON.stringify(
										item,
										(k, v) => (k === '_attributes' ? undefined : v),
										2
									)}</pre>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>
