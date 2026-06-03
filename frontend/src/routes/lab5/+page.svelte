<script lang="ts">
	import { calculateFeeApiV1LabApiLabCalculateFeePost } from '$lib/api/generated/endpoints';

	let amount = $state<number>(1000);
	let campaignType = $state<string>('volunteer');

	let loading = $state(false);
	let error = $state<string>('');
	let result = $state<any>(null);

	async function calculateFee(e: Event) {
		e.preventDefault();
		if (amount <= 0) {
			error = 'Сума має бути більшою за нуль';
			return;
		}

		loading = true;
		error = '';
		result = null;

		try {
			// Викликаємо згенеровану функцію Orval
			const response = await calculateFeeApiV1LabApiLabCalculateFeePost({
				amount: amount,
				campaign_type: campaignType
			});

			// customInstance повертає дані безпосередньо
			result = response;
		} catch (err: any) {
			console.error('Calculate Error:', err);
			error = err?.response?.data?.detail || 'Сталася помилка при розрахунку транзакції';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Лабораторна №5: Патерн Strategy</title>
</svelte:head>

<div class="mx-auto max-w-3xl p-6">
	<div class="mb-8">
		<h1 class="text-3xl font-bold tracking-tight text-slate-900">Калькулятор транзакцій</h1>
	</div>

	<div class="grid gap-8 md:grid-cols-2">
		<!-- Форма -->
		<div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
			<form onsubmit={calculateFee} class="space-y-6">
				<!-- Поле: Сума -->
				<div class="space-y-2">
					<label for="amount" class="block text-sm font-medium text-slate-700"
						>Сума донату (₴)</label
					>
					<input
						id="amount"
						type="number"
						min="1"
						step="0.01"
						bind:value={amount}
						required
						class="block w-full rounded-lg border border-slate-300 p-2.5 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
					/>
				</div>

				<!-- Поле: Тип кампанії -->
				<div class="space-y-3">
					<span class="block text-sm font-medium text-slate-700">Тип збору</span>
					<div class="space-y-2">
						<label
							class="flex cursor-pointer items-center space-x-3 rounded-lg border p-3 hover:bg-slate-50"
						>
							<input
								type="radio"
								name="campaign_type"
								value="volunteer"
								bind:group={campaignType}
								class="h-4 w-4 border-slate-300 text-blue-600 focus:ring-blue-600"
							/>
							<span class="text-sm text-slate-900">Волонтерський збір (Комісія 0%)</span>
						</label>

						<label
							class="flex cursor-pointer items-center space-x-3 rounded-lg border p-3 hover:bg-slate-50"
						>
							<input
								type="radio"
								name="campaign_type"
								value="private"
								bind:group={campaignType}
								class="h-4 w-4 border-slate-300 text-blue-600 focus:ring-blue-600"
							/>
							<span class="text-sm text-slate-900">Приватний збір (Комісія 1%)</span>
						</label>
					</div>
				</div>

				<!-- Кнопка сабміту -->
				<button
					type="submit"
					disabled={loading}
					class="flex w-full justify-center rounded-lg border border-transparent bg-blue-600 px-4 py-3 text-sm font-medium text-white shadow-sm transition-colors hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none disabled:cursor-not-allowed disabled:bg-blue-400"
				>
					{#if loading}
						Розрахунок...
					{:else}
						Розрахувати транзакцію
					{/if}
				</button>
			</form>
		</div>

		<!-- Результат -->
		<div class="flex flex-col">
			{#if error}
				<div class="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
					<h3 class="font-medium">Помилка</h3>
					<p class="mt-1 text-sm">{error}</p>
				</div>
			{/if}

			{#if result}
				<div class="rounded-2xl border border-emerald-200 bg-emerald-50 p-6 shadow-sm">
					<h3 class="mb-4 text-lg font-semibold text-emerald-900">Результат розрахунку</h3>

					<dl class="space-y-4">
						<div class="flex items-center justify-between border-b border-emerald-200/50 pb-3">
							<dt class="text-sm font-medium text-emerald-800">Оригінальна сума</dt>
							<dd class="text-base font-semibold text-emerald-900">
								{result.original_amount.toFixed(2)} ₴
							</dd>
						</div>

						<div class="flex items-center justify-between border-b border-emerald-200/50 pb-3">
							<dt class="text-sm font-medium text-emerald-800">Комісія платформи</dt>
							<dd class="text-base font-semibold text-emerald-900">{result.fee.toFixed(2)} ₴</dd>
						</div>

						<div class="flex items-center justify-between border-b border-emerald-200/50 pb-3">
							<dt class="text-sm font-bold text-emerald-900">Разом до оплати</dt>
							<dd class="text-xl font-black text-emerald-900">
								{result.total_amount.toFixed(2)} ₴
							</dd>
						</div>

						<div class="pt-2">
							<dt class="mb-1 text-xs font-medium tracking-wider text-emerald-700 uppercase">
								Використана стратегія (Бекенд)
							</dt>
							<dd
								class="inline-flex items-center rounded-full bg-emerald-100 px-3 py-1 font-mono text-xs font-medium text-emerald-800"
							>
								{result.strategy_used}
							</dd>
						</div>
					</dl>
				</div>
			{:else if !loading && !error}
				<div
					class="flex h-full items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-6 text-center"
				>
					<p class="text-sm text-slate-500">Заповніть форму та натисніть "Розрахувати"</p>
				</div>
			{/if}
		</div>
	</div>
</div>
