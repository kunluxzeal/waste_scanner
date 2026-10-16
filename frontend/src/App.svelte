<script>
  import { onMount } from 'svelte';
  import Home from './pages/Home.svelte';
  import Analyze from './pages/Analyze.svelte';
  import Settings from './pages/Settings.svelte';
  import './app.css';

  let page = getPageFromPath();

  function getPageFromPath() {
    const path = window.location.pathname.replace(/\/+$/, '') || '/';

    if (path === '/analyze') return 'Analyze';
    if (path === '/settings') return 'Settings';

    return 'Home';
  }

  function navigate(path) {
    if (window.location.pathname !== path) {
      window.history.pushState({}, '', path);
    }

    page = getPageFromPath();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function handlePopState() {
    page = getPageFromPath();
  }

  onMount(() => {
    window.addEventListener('popstate', handlePopState);

    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  });
</script>

<svelte:head>
  <title>
    {page === 'Home'
      ? 'EcoSort | AI Waste Scanner'
      : page === 'Analyze'
        ? 'Analyze Waste | EcoSort'
        : 'Settings | EcoSort'}
  </title>

  <meta
    name="description"
    content="EcoSort uses AI object detection to identify electronic waste."
  />
  <meta name="theme-color" content="#0b1017" />
</svelte:head>

<div class="site-shell">
  <header class="site-header">
    <a
      class="brand"
      href="/"
      onclick={(event) => {
        event.preventDefault();
        navigate('/');
      }}
    >
      <span class="brand-icon">E</span>

      <span class="brand-copy">
        <strong>EcoSort</strong>
        <small>AI WASTE SCANNER</small>
      </span>
    </a>

    <nav class="top-navigation" aria-label="Main navigation">
      <a
        href="/"
        class:active={page === 'Home'}
        aria-current={page === 'Home' ? 'page' : undefined}
        onclick={(event) => {
          event.preventDefault();
          navigate('/');
        }}
      >
        Home
      </a>

      <a
        href="/analyze"
        class:active={page === 'Analyze'}
        aria-current={page === 'Analyze' ? 'page' : undefined}
        onclick={(event) => {
          event.preventDefault();
          navigate('/analyze');
        }}
      >
        Analyze
      </a>

      <a
        href="/settings"
        class:active={page === 'Settings'}
        aria-current={page === 'Settings' ? 'page' : undefined}
        onclick={(event) => {
          event.preventDefault();
          navigate('/settings');
        }}
      >
        Settings
      </a>
    </nav>

    <div class="header-brand-label">
      <span class="brand-status"></span>
      Edge AI
    </div>
  </header>

  <main class="page-container">
    {#if page === 'Home'}
      <Home onNavigate={navigate} />
    {:else if page === 'Analyze'}
      <Analyze onNavigate={navigate} />
    {:else}
      <Settings onNavigate={navigate} />
    {/if}
  </main>

  <footer class="site-footer">
    <span>EcoSort · AI waste identification</span>
    <span>Powered by edge AI</span>
  </footer>
</div>