<script lang="ts">
	import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Label } from '$lib/components/ui/label';
	import { Switch } from '$lib/components/ui/switch';

	// ==========================================
	// Загальне Завдання 6: Перетворення рядків/файлів до формату HTML та навпаки
	// ==========================================

	// З Тексту в HTML
	let rawTextToHtml = $state(
		'Привіт!\nЦе **жирний текст** та *курсив*.\nПеренесення рядків також працює.'
	);
	let convertedHtml = $derived.by(() => {
		if (!rawTextToHtml) return '';
		return rawTextToHtml
			.replace(/&/g, '&amp;') // Екранування
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;')
			.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Жирний
			.replace(/\*(.*?)\*/g, '<em>$1</em>') // Курсив
			.replace(/\n/g, '<br>'); // Перенесення рядків
	});

	// З HTML в звичайний текст
	let htmlToRawText = $state(
		"<p>Це <strong>HTML</strong> код із <a href='https://test.com'>посиланням</a>.</p><br>Другий рядок."
	);
	let convertedText = $derived.by(() => {
		if (!htmlToRawText) return '';
		return htmlToRawText
			.replace(/<br\s*\/?>/gi, '\n') // Заміна <br> на перенесення рядка
			.replace(/<[^>]+>/g, ''); // Видалення всіх інших HTML-тегів
	});

	// ==========================================
	// Загальне Завдання 7: Перевірка синтаксичної правильності e-mail
	// ==========================================
	let emailToValidate = $state('correct.email@example.com');
	let isEmailValid = $derived.by(() => {
		// Суворий regex для перевірки цілого рядка (від ^ до $)
		const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
		return regex.test(emailToValidate);
	});

	// ==========================================
	// Блок 1. Завдання 14: Витягнути нікнейм, домен та суфікс з e-mail
	// ==========================================
	let emailToParse = $state('student@university.edu.ua');
	let parsedEmailResult = $derived.by(() => {
		const regex = /^([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})$/;
		const match = emailToParse.match(regex);
		if (match) {
			return { nickname: match[1], domain: match[2], suffix: match[3] };
		}
		return null;
	});

	// ==========================================
	// Блок 1. Завдання 16: Знайти в тексті адресу е-mail
	// ==========================================
	let textWithEmails = $state("Зв'яжіться з нами за адресою info@example.com або support@test.ua.");
	let foundEmails = $derived.by(() => {
		const regex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
		return textWithEmails.match(regex) || [];
	});

	// ==========================================
	// Блок 2. Завдання 2: Проаналізувати лог-файл (остання дія та вхід)
	// ==========================================
	let logText = $state(
		`2026-05-19 10:00:00 [LOGIN] user_id=123
2026-05-19 10:05:00 [ACTION] user_id=123 action=upload_file
2026-05-19 10:15:00 [ACTION] user_id=123 action=delete_file`
	);

	let logAnalysis = $derived.by(() => {
		const loginRegex = /(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[LOGIN\]/g;
		const actionRegex = /(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[ACTION\].*?action=(\w+)/g;

		let lastLoginTime = null;
		let lastActionTime = null;
		let lastActionName = null;

		let loginMatch;
		while ((loginMatch = loginRegex.exec(logText)) !== null) {
			lastLoginTime = loginMatch[1];
		}

		let actionMatch;
		while ((actionMatch = actionRegex.exec(logText)) !== null) {
			lastActionTime = actionMatch[1];
			lastActionName = actionMatch[2];
		}

		return { lastLoginTime, lastActionTime, lastActionName };
	});

	// ==========================================
	// Блок 2. Завдання 22: Отримати відомості щодо характеристик браузеру користувача.
	// ==========================================
	let userAgentString = $state('');

	$effect(() => {
		if (typeof window !== 'undefined' && !userAgentString) {
			userAgentString = navigator.userAgent;
		}
	});

	const BROWSER_NAME_MAP: Record<string, string> = {
		CriOS: 'Chrome (iOS)',
		FxiOS: 'Firefox (iOS)',
		OPT: 'Opera Mini',
		OPR: 'Opera',
		SamsungBrowser: 'Samsung Browser',
		Edg: 'Edge',
		EdgA: 'Edge',
		EdgiOS: 'Edge (iOS)',
		Trident: 'Internet Explorer',
		MSIE: 'Internet Explorer'
	};

	const WINDOWS_VERSION_MAP: Record<string, string> = {
		'10.0': '10 / 11',
		'6.3': '8.1',
		'6.2': '8',
		'6.1': '7',
		'6.0': 'Vista',
		'5.1': 'XP'
	};

	let browserInfo = $derived.by(() => {
		if (!userAgentString) {
			return {
				browser: 'Невідомо',
				browserVersion: '',
				os: 'Невідомо',
				osVersion: '',
				device: 'Desktop',
				engine: 'Невідомо',
				engineVersion: '',
				isBrave: false
			};
		}

		const ua = userAgentString;

		const browserRegex =
			/(?<browser>SamsungBrowser|CriOS|FxiOS|OPT|OPR|EdgA|EdgiOS|Edg|MSIE|Trident|Firefox|Chrome|Safari)\/(?<version>\d+(?:\.\d+)?)/i;
		const osRegex =
			/(?<os>Windows NT|Mac OS X|CrOS|Android|Linux|iPhone OS|iPad.*?OS)\s*(?<version>[\d._]+)?/i;
		const engineRegex = /(?<engine>AppleWebKit|Gecko|Trident|Presto)\/(?<version>\d+(?:\.\d+)?)/i;

		const browserMatch = ua.match(browserRegex);
		const osMatch = ua.match(osRegex);
		const engineMatch = ua.match(engineRegex);

		let rawBrowser = browserMatch?.groups?.browser ?? 'Невідомо';
		let browserVersion = browserMatch?.groups?.version ?? '';
		let browserName = BROWSER_NAME_MAP[rawBrowser] ?? rawBrowser;

		const isBrave = typeof navigator !== 'undefined' && 'brave' in navigator;
		if (isBrave) browserName = 'Brave';

		let osName = osMatch?.groups?.os ?? 'Невідомо';
		let osVersion = osMatch?.groups?.version ? osMatch.groups.version.replace(/_/g, '.') : '';

		if (osName === 'Windows NT') {
			osName = 'Windows';
			osVersion = WINDOWS_VERSION_MAP[osVersion] ?? osVersion;
		} else if (osName === 'Mac OS X') {
			osName = 'macOS';
		} else if (osName === 'iPhone OS' || osName.startsWith('iPad')) {
			osName = 'iOS';
		} else if (osName === 'CrOS') {
			osName = 'Chrome OS';
			osVersion = '';
		}

		const isTablet = /iPad|Android(?!.*Mobile)/i.test(ua);
		const isMobile = !isTablet && /Mobile|Android|iPhone|iPod/i.test(ua);

		let device = 'Desktop';
		if (isTablet) device = 'Tablet';
		else if (isMobile) device = 'Mobile';

		return {
			browser: browserName,
			browserVersion,
			os: osName,
			osVersion,
			device,
			engine: engineMatch?.groups?.engine ?? 'Невідомо',
			engineVersion: engineMatch?.groups?.version ?? '',
			isBrave
		};
	});

	// ==========================================
	// Блок 3. Завдання 6: Витягти всі посилання з HTML
	// ==========================================
	let htmlSnippet = $state(
		`<p>Ось <a href="https://google.com">посилання в тезі</a>.</p>
<img src="/images/pic.png" alt="картинка">
<div>А тут просто текст: https://wikipedia.org/wiki/HTML і все.</div>
<script src="https://cdn.example.com/app.js"><\/script>`
	);

	let includeTextLinks = $state(false);

	let extractedLinks = $derived.by(() => {
		const links: string[] = [];

		const attrRegex = /(?:href|src)\s*=\s*["']([^"']+)["']/gi;
		let attrMatch;
		while ((attrMatch = attrRegex.exec(htmlSnippet)) !== null) {
			links.push(attrMatch[1]);
		}

		if (includeTextLinks) {
			const textRegex = /(?<!["'=])\b(https?:\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\/[^\s<"']*)?)\b/gi;
			let textMatch;
			while ((textMatch = textRegex.exec(htmlSnippet)) !== null) {
				links.push(textMatch[1]);
			}
		}

		return [...new Set(links)];
	});
</script>

<div class="container mx-auto space-y-6 p-6">
	<h1 class="mb-8 text-3xl font-bold">Лабораторна робота: Регулярні вирази</h1>

	<Card>
		<CardHeader>
			<CardTitle>Завдання 6. Текст &harr; HTML</CardTitle>
		</CardHeader>
		<CardContent class="space-y-6">
			<div class="space-y-4">
				<div class="space-y-2">
					<Label for="rawText">Звичайний текст (з підтримкою **жирного** та *курсиву*)</Label>
					<Textarea id="rawText" bind:value={rawTextToHtml} rows={3} />
				</div>
				<div class="rounded-md bg-muted p-4">
					<p class="mb-2 text-sm text-muted-foreground">Результат (HTML):</p>
					<div class="font-mono text-sm break-all">{convertedHtml}</div>
				</div>
			</div>

			<hr />

			<div class="space-y-4">
				<div class="space-y-2">
					<Label for="htmlText">HTML код (для очищення від тегів)</Label>
					<Textarea id="htmlText" bind:value={htmlToRawText} rows={3} class="font-mono" />
				</div>
				<div class="rounded-md bg-muted p-4">
					<p class="mb-2 text-sm text-muted-foreground">Результат (Текст):</p>
					<div class="whitespace-pre-wrap">{convertedText}</div>
				</div>
			</div>
		</CardContent>
	</Card>

	<Card>
		<CardHeader>
			<CardTitle>Завдання 7. Перевірка синтаксичної правильності e-mail</CardTitle>
		</CardHeader>
		<CardContent class="space-y-4">
			<div class="space-y-2">
				<Label for="email7">Введіть e-mail для валідації</Label>
				<Input id="email7" bind:value={emailToValidate} />
			</div>
			<div
				class="rounded-md p-4 {isEmailValid
					? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
					: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'}"
			>
				<strong>Статус:</strong>
				{isEmailValid ? '✅ Синтаксис правильний' : '❌ Помилка в синтаксисі e-mail'}
			</div>
		</CardContent>
	</Card>

	<Card>
		<CardHeader>
			<CardTitle>1.14 Витягнути дані з e-mail адреси</CardTitle>
		</CardHeader>
		<CardContent class="space-y-4">
			<div class="space-y-2">
				<Label for="email14">E-mail для розбору</Label>
				<Input id="email14" bind:value={emailToParse} />
			</div>
			<div class="rounded-md bg-muted p-4">
				{#if parsedEmailResult}
					<p><strong>Нікнейм:</strong> {parsedEmailResult.nickname}</p>
					<p><strong>Домен:</strong> {parsedEmailResult.domain}</p>
					<p><strong>Суфікс:</strong> {parsedEmailResult.suffix}</p>
				{:else}
					<p class="text-destructive">Некоректний формат e-mail.</p>
				{/if}
			</div>
		</CardContent>
	</Card>

	<Card>
		<CardHeader>
			<CardTitle>1.16 Знайти e-mail адреси в тексті</CardTitle>
		</CardHeader>
		<CardContent class="space-y-4">
			<div class="space-y-2">
				<Label for="text16">Текст</Label>
				<Textarea id="text16" bind:value={textWithEmails} rows={3} />
			</div>
			<div class="rounded-md bg-muted p-4">
				<p><strong>Знайдені адреси:</strong></p>
				{#if foundEmails.length > 0}
					<ul class="list-disc pl-5">
						{#each foundEmails as email (email)}
							<li>{email}</li>
						{/each}
					</ul>
				{:else}
					<p class="text-muted-foreground">Адрес не знайдено.</p>
				{/if}
			</div>
		</CardContent>
	</Card>

	<Card>
		<CardHeader>
			<CardTitle>2.2 Аналіз лог-файлу користувача</CardTitle>
		</CardHeader>
		<CardContent class="space-y-4">
			<div class="space-y-2">
				<Label for="logs2">Логи</Label>
				<Textarea id="logs2" bind:value={logText} rows={5} class="font-mono text-sm" />
			</div>
			<div class="rounded-md bg-muted p-4">
				<p><strong>Останній вхід (LOGIN):</strong> {logAnalysis.lastLoginTime || 'Не знайдено'}</p>
				<p>
					<strong>Остання дія:</strong>
					{logAnalysis.lastActionName || 'Не знайдено'}
					<span class="text-muted-foreground"
						>({logAnalysis.lastActionTime || 'Час невідомий'})</span
					>
				</p>
			</div>
		</CardContent>
	</Card>

	<Card>
		<CardHeader>
			<CardTitle>2.22 Характеристики браузеру користувача</CardTitle>
		</CardHeader>
		<CardContent class="space-y-4">
			<div class="space-y-2">
				<Label for="ua22">User-Agent рядок</Label>
				<Textarea id="ua22" bind:value={userAgentString} rows={2} class="font-mono text-sm" />
			</div>
			<div class="rounded-md bg-muted p-4">
				<p><strong>Браузер:</strong> {browserInfo.browser} {browserInfo.browserVersion}</p>
				<p><strong>ОС:</strong> {browserInfo.os} {browserInfo.osVersion}</p>
				<p><strong>Пристрій:</strong> {browserInfo.device}</p>
				<p><strong>Рендер-движок:</strong> {browserInfo.engine} {browserInfo.engineVersion}</p>
				{#if browserInfo.isBrave}
					<p class="mt-2 text-green-600"><em>Виявлено браузер Brave</em></p>
				{/if}
			</div>
		</CardContent>
	</Card>

	<Card>
		<CardHeader>
			<CardTitle>3.6 Витягти посилання з HTML</CardTitle>
		</CardHeader>
		<CardContent class="space-y-4">
			<div class="space-y-2">
				<Label for="html6">HTML Код</Label>
				<Textarea id="html6" bind:value={htmlSnippet} rows={5} class="font-mono text-sm" />
			</div>

			<div class="flex items-center space-x-2 py-2">
				<Switch id="mode-switch" bind:checked={includeTextLinks} />
				<Label for="mode-switch" class="cursor-pointer">
					Витягувати також звичайні текстові URL (не в атрибутах)
				</Label>
			</div>

			<div class="rounded-md bg-muted p-4">
				<p class="mb-2"><strong>Знайдені ресурси (URL):</strong></p>
				{#if extractedLinks.length > 0}
					<ul class="list-disc space-y-1 pl-5">
						{#each extractedLinks as link (link)}
							<li class="font-mono text-sm break-all text-primary">{link}</li>
						{/each}
					</ul>
				{:else}
					<p class="text-muted-foreground">Посилання не знайдені.</p>
				{/if}
			</div>
		</CardContent>
	</Card>
</div>
