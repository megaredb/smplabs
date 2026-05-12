<script lang="ts">
    import './app.css'; 
    import { onMount } from 'svelte';

    let { children } = $props();
    
    let isLoggedIn = $state(false);

    onMount(() => {
        if (localStorage.getItem('access_token')) {
            isLoggedIn = true;
        }
    });

    function logout() {
        localStorage.removeItem('access_token');
        isLoggedIn = false;
        window.location.href = '/';
    }
</script>

<div class="min-h-screen flex flex-col bg-gray-50 text-slate-800 font-sans">
    <header class="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex-shrink-0">
                <a href="/" class="text-2xl font-bold text-blue-600 tracking-tight">RazomFund</a>
            </div>
            
            <nav class="hidden md:flex space-x-6 items-center">
                <a href="/" class="text-gray-600 hover:text-blue-600 font-medium transition-colors">Головна</a>
                <a href="/campaigns" class="text-gray-600 hover:text-blue-600 font-medium transition-colors">Збори</a>
                
                {#if isLoggedIn}
                    <button onclick={logout} class="text-red-600 font-medium hover:text-red-700 transition-colors ml-4">Вийти</button>
                {:else}
                    <div class="flex items-center space-x-4 ml-4 border-l border-gray-200 pl-4">
                        <a href="/login" class="text-gray-600 hover:text-blue-600 font-medium transition-colors">Увійти</a>
                        <a href="/register" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors shadow-sm">Реєстрація</a>
                    </div>
                {/if}
            </nav>
        </div>
    </header>

    <main class="flex-grow w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {@render children()}
    </main>

    <footer class="bg-white border-t border-gray-200 mt-auto">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-gray-500 text-sm">
            &copy; 2026 RazomFund Platform. Усі права захищено.
        </div>
    </footer>
</div>