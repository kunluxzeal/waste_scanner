<script>
  import { onMount } from 'svelte';

  let { onNavigate } = $props();
  let cameraOnline = $state(false);
  let cameraStatus = $state('Checking camera...');
  let loading = $state(false);
  let error = $state('');
  let result = $state(null);
  let cameraError = false;
  let requestInProgress = false;

  const cameraStream = '/api/v1/camera/stream';
  const statusEndpoint = '/api/v1/camera/status';
  const snapshotEndpoint = '/api/v1/camera/snapshot';
  const detectionEndpoint = '/api/v1/detect';

  async function checkCamera() {
    try {
      const response = await fetch(statusEndpoint, {
        cache: 'no-store'
      });

      if (!response.ok) {
        throw new Error('Camera status API unavailable');
      }

      const data = await response.json();

      cameraOnline =
        data.camera_running === true &&
        data.frame_available === true;

      cameraStatus = cameraOnline
        ? 'Camera connected and streaming'
        : data.error || (
            data.camera_running
              ? 'Waiting for camera frame'
              : 'Camera offline'
          );

      cameraError = !data.camera_running;
    } catch (err) {
      cameraOnline = false;
      cameraError = true;
      cameraStatus = 'Unable to reach camera status API';
    }
  }

  async function analyzeWaste() {
    if (requestInProgress) return;

    requestInProgress = true;
    loading = true;
    error = '';
    result = null;

    try {
      const snapshotResponse = await fetch(snapshotEndpoint, {
        cache: 'no-store'
      });

      if (!snapshotResponse.ok) {
        const data = await snapshotResponse.json().catch(() => ({}));

        throw new Error(
          data.detail ||
          `Camera snapshot failed (${snapshotResponse.status}).`
        );
      }

      const imageBlob = await snapshotResponse.blob();

      if (!imageBlob.size) {
        throw new Error('The camera returned an empty image.');
      }

      const formData = new FormData();
      formData.append('file', imageBlob, 'ecosort-snapshot.jpg');

      const response = await fetch(detectionEndpoint, {
        method: 'POST',
        body: formData
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(
          data.detail || `Detection failed (${response.status}).`
        );
      }

      result = data;
    } catch (err) {
      error = err instanceof Error
        ? err.message
        : 'Could not analyze the image.';
    } finally {
      loading = false;
      requestInProgress = false;
    }
  }

  onMount(() => {
    checkCamera();

    const timer = window.setInterval(checkCamera, 10000);

    return () => window.clearInterval(timer);
  });
</script>

<section class="page-intro">
  <div>
    <div class="eyebrow"><span></span> LIVE CAMERA ANALYSIS</div>
    <h1>Analyze waste</h1>
    <p>
      Position one electronic waste item clearly in front of the camera.
    </p>
  </div>

  <button class="secondary-button" onclick={checkCamera}>
    Refresh status ↻
  </button>
</section>

<section class="analyze-layout">
  <article class="content-panel camera-panel">
    <div class="panel-heading">
      <div>
        <h2>Camera preview</h2>
        <p>Live feed from your Raspberry Pi camera</p>
      </div>

      <span class:offline={!cameraOnline} class="live-badge">
        <span></span>
        {cameraOnline ? 'LIVE' : 'OFFLINE'}
      </span>
    </div>

    <div class="camera-frame">
      <img
        src={cameraStream}
        alt="Live EcoSort camera feed with object detection annotations"
        onerror={() => {
          cameraOnline = false;
          cameraError = true;
          cameraStatus = 'Camera stream unavailable';
        }}
        onload={() => {
          cameraError = false;
        }}
      />

      <div class="frame-overlay" aria-hidden="true">
        <span class="frame-corner tl"></span>
        <span class="frame-corner tr"></span>
        <span class="frame-corner bl"></span>
        <span class="frame-corner br"></span>
      </div>
    </div>

    <div class="camera-footer">
      <span>
        <span class:online={cameraOnline} class="status-dot"></span>
        {cameraStatus}
      </span>
      <span>Raspberry Pi</span>
    </div>

    <button
      class="primary-button full-button"
      disabled={loading}
      onclick={analyzeWaste}
    >
      {loading ? 'Analyzing image...' : '◎ Analyze Waste Item'}
    </button>

    <p class="privacy-note">
      AI inference runs on the local backend, provided the API is
      deployed on your Raspberry Pi.
    </p>
  </article>

  <article class="content-panel results-panel">
    <div class="panel-heading">
      <div>
        <h2>Analysis results</h2>
        <p>YOLO object detection output</p>
      </div>
      <span class="result-symbol">✳</span>
    </div>

    {#if loading}
      <div class="empty-state">
        <div class="loader"></div>
        <h3>Analyzing image</h3>
        <p>Running the detection model on the captured frame.</p>
      </div>

    {:else if error}
      <div class="message-state error-state">
        <div class="empty-icon">!</div>
        <h3>Analysis failed</h3>
        <p>{error}</p>
        <button class="secondary-button" onclick={analyzeWaste}>
          Try again
        </button>
      </div>

    {:else if result}
      <div class="result-content">
        <div class="success-mark">✓</div>
        <span class="stat-label">MODEL RESPONSE</span>
        <h3>Detection complete</h3>

        <div class="detection-summary">
          <div class="detection-metric">
            <span>Objects found</span>
            <strong>{result.detection_count}</strong>
          </div>

          <div class="detection-metric">
            <span>Inference time</span>
            <strong>{result.inference_time_ms} ms</strong>
          </div>

          <div class="detection-metric">
            <span>Image size</span>
            <strong>{result.image_width} × {result.image_height}</strong>
          </div>

          <div class="detection-metric">
            <span>Model</span>
            <strong>{result.model}</strong>
          </div>
        </div>

        {#if result.detections?.length}
          <div class="detected-items">
            <h3>Detected objects</h3>

            {#each result.detections as detection, i (`${detection.class_id}-${i}`)}
              <article class="detected-item">
                <div class="detected-item-heading">
                  <div>
                    <span class="item-index">ITEM {i + 1}</span>
                    <h4>{detection.class_name}</h4>
                  </div>

                  <span class="confidence-badge">
                    {(detection.confidence * 100).toFixed(1)}%
                  </span>
                </div>

                <div class="confidence-track">
                  <div
                    class="confidence-fill"
                    style={`width: ${Math.max(0, Math.min(100, detection.confidence * 100))}%`}
                  ></div>
                </div>

                <details class="bbox-details">
                  <summary>View bounding box</summary>

                  <div class="bbox-values">
                    <span>X1: {detection.bbox.x1}</span>
                    <span>Y1: {detection.bbox.y1}</span>
                    <span>X2: {detection.bbox.x2}</span>
                    <span>Y2: {detection.bbox.y2}</span>
                  </div>
                </details>
              </article>
            {/each}
          </div>
        {:else}
          <div class="no-detections">
            <div class="empty-icon">◎</div>
            <h3>No objects detected</h3>
            <p>
              Try repositioning the item or improving the lighting.
            </p>
          </div>
        {/if}
      </div>

    {:else}
      <div class="empty-state">
        <div class="empty-icon">◎</div>
        <h3>No analysis yet</h3>
        <p>
          Place an item in the camera view, then select Analyze Waste Item.
        </p>
      </div>
    {/if}
  </article>
</section>

<div class="back-navigation">
  <button class="text-button" onclick={() => onNavigate('/')}>
    ← Back to Home
  </button>
  <button class="text-button" onclick={() => onNavigate('/settings')}>
    Device Settings →
  </button>
</div>