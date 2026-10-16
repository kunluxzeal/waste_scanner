<script>
  import { onMount } from 'svelte';

  let { onNavigate } = $props();

  let loading = $state(false);
  let cameraOnline = $state(false);
  let cameraStatus = $state('Checking camera...');
  let cameraError = $state('');
  let inferenceTime = $state(0);
  let captureFps = $state(0);

  let frameAvailable = false;

  async function refreshStatus() {
    loading = true;

    try {
      const response = await fetch('/api/v1/camera/status', {
        cache: 'no-store'
      });

      if (!response.ok) {
        throw new Error('Unable to connect to the FastAPI backend.');
      }

      const data = await response.json();

      frameAvailable = data.frame_available === true;
      cameraOnline = data.camera_running === true && frameAvailable;
      cameraStatus = cameraOnline
        ? 'Connected and streaming'
        : data.error || 'Camera unavailable';

      cameraError = data.error || '';
      inferenceTime = data.inference_time_ms ?? 0;
      captureFps = data.capture_fps ?? 0;
    } catch (err) {
      cameraOnline = false;
      frameAvailable = false;
      cameraStatus = 'Backend connection failed';
      cameraError = err instanceof Error
        ? err.message
        : 'Unknown connection error';
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    refreshStatus();

    const timer = window.setInterval(refreshStatus, 10000);

    return () => window.clearInterval(timer);
  });
</script>

<section class="page-intro">
  <div>
    <div class="eyebrow"><span></span> SYSTEM CONFIGURATION</div>
    <h1>Settings</h1>
    <p>Monitor the camera and the EcoSort backend running on your device.</p>
  </div>

  <button class="secondary-button" onclick={refreshStatus}>
    Refresh ↻
  </button>
</section>

<section class="settings-grid">
  <article class="content-panel settings-card">
    <div class="settings-card-icon">◎</div>
    <span class="stat-label">CAMERA STATUS</span>
    <h2>{cameraOnline ? 'Connected' : 'Unavailable'}</h2>
    <p>{cameraStatus}</p>
    <span class:online={cameraOnline} class="status-dot"></span>
  </article>

  <article class="content-panel settings-card">
    <div class="settings-card-icon">◈</div>
    <span class="stat-label">DETECTION ENGINE</span>
    <h2>YOLO26n-NCNN</h2>
    <p>Object detection through the FastAPI backend.</p>
  </article>

  <article class="content-panel settings-card">
    <div class="settings-card-icon">⌁</div>
    <span class="stat-label">INFERENCE TIME</span>
    <h2>{inferenceTime} ms</h2>
    <p>Most recent camera inference reported by the backend.</p>
  </article>

  <article class="content-panel settings-card">
    <div class="settings-card-icon">▣</div>
    <span class="stat-label">CAPTURE RATE</span>
    <h2>{captureFps} FPS</h2>
    <p>Approximate camera worker processing rate.</p>
  </article>
</section>

<section class="content-panel configuration-panel">
  <div class="panel-heading">
    <div>
      <h2>Backend configuration</h2>
      <p>Endpoints used by the Svelte application.</p>
    </div>
    <span class="setting-value">{loading ? 'Checking...' : 'Status checked'}</span>
  </div>

  <div class="configuration-row">
    <div>
      <h3>Camera status</h3>
      <p>Checks the camera worker and latest frame availability.</p>
    </div>
    <code>/api/v1/camera/status</code>
  </div>

  <div class="configuration-row">
    <div>
      <h3>Live camera stream</h3>
      <p>MJPEG stream with object detection annotations.</p>
    </div>
    <code>/api/v1/camera/stream</code>
  </div>

  <div class="configuration-row">
    <div>
      <h3>Object detection</h3>
      <p>Accepts an image as multipart form data.</p>
    </div>
    <code>/api/v1/detect</code>
  </div>

  {#if cameraError}
    <div class="settings-error">
      <strong>Connection details</strong>
      <p>{cameraError}</p>
    </div>
  {/if}
</section>

<section class="settings-cta">
  <div>
    <h2>Ready to identify an item?</h2>
    <p>Return to the scanner to capture and analyze waste.</p>
  </div>

  <button
    class="primary-button"
    onclick={() => onNavigate('/analyze')}
  >
    Open Analyzer →
  </button>
</section>

<div class="back-navigation">
  <button class="text-button" onclick={() => onNavigate('/')}>
    ← Back to Home
  </button>
</div>