<script lang="ts">
    import { Button } from '$lib/components/ui/button';
    import { ArrowRight, Heart, ShieldCheck, Zap } from '@lucide/svelte';
    import { resolve } from '$app/paths';
</script>

<svelte:head>
    <title>RazomFund - Платформа благодійних зборів</title>
</svelte:head>

<div class="flex flex-col items-center justify-center min-h-[70vh] text-center space-y-12">
    <div class="space-y-6 max-w-3xl">
        <h1 class="text-5xl sm:text-6xl font-extrabold tracking-tight text-slate-900 leading-tight">
            Допомагайте тим, хто <br/>
            <span class="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">потребує цього найбільше</span>
        </h1>
        <p class="text-xl text-slate-600 leading-relaxed max-w-2xl mx-auto">
            RazomFund - це сучасна та прозора платформа для створення та підтримки благодійних зборів. Зробіть свій внесок у добру справу вже сьогодні.
        </p>
        <div class="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
            <Button size="lg" href={resolve("/campaigns")} class="bg-blue-600 hover:bg-blue-700 w-full sm:w-auto text-lg px-8 py-6 gap-2 rounded-full shadow-lg hover:shadow-xl transition-all">
                Переглянути збори
                <ArrowRight class="w-5 h-5" />
            </Button>
            <Button size="lg" variant="outline" href={resolve("/campaigns/create")} class="w-full sm:w-auto text-lg px-8 py-6 rounded-full border-slate-300">
                Створити збір
            </Button>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl pt-12 border-t border-slate-200/60 mt-12">
        <div class="flex flex-col items-center text-center space-y-3 p-6">
            <div class="bg-blue-100 p-4 rounded-2xl mb-2 text-blue-600">
                <ShieldCheck class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-bold text-slate-900">Прозорість</h3>
            <p class="text-slate-600">Кожна транзакція та звітність доступна для перегляду всім учасникам.</p>
        </div>
        <div class="flex flex-col items-center text-center space-y-3 p-6">
            <div class="bg-indigo-100 p-4 rounded-2xl mb-2 text-indigo-600">
                <Zap class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-bold text-slate-900">Швидкість</h3>
            <p class="text-slate-600">Зручний інтерфейс дозволяє створити збір або задонатити за лічені хвилини.</p>
        </div>
        <div class="flex flex-col items-center text-center space-y-3 p-6">
            <div class="bg-rose-100 p-4 rounded-2xl mb-2 text-rose-600">
                <Heart class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-bold text-slate-900">Довіра</h3>
            <p class="text-slate-600">Ми працюємо тільки з перевіреними організаторами та фондами.</p>
        </div>
    </div>
</div>
