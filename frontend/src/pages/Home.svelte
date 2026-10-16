<script>
  let { onNavigate } = $props();
</script>

<section class="home-hero">
  <div class="hero-copy">
    <div class="eyebrow">
      <span></span>
      INTELLIGENT WASTE IDENTIFICATION
    </div>

    <h1>
      Make e-waste visible.
      <em>Make impact.</em>
    </h1>

    <p class="hero-description">
      Identify electronic waste with AI-powered object detection.
      Scan an item, view its predicted category, and use the results
      to support better recycling and disposal decisions.
    </p>

    <button
      class="primary-button"
      onclick={() => onNavigate('/analyze')}
    >
      Analyze Waste
      <span aria-hidden="true">↗</span>
    </button>

    <div class="hero-note">
      <span class="brand-status"></span>
      Designed for local Raspberry Pi processing
    </div>
  </div>

  <div class="hero-visual" aria-label="AI scanner illustration">
    <div class="hero-orbit orbit-outer"></div>
    <div class="hero-orbit orbit-inner"></div>

    <div class="scanner-device">
      <div class="scanner-screen">
        <span class="scanner-corner corner-tl"></span>
        <span class="scanner-corner corner-tr"></span>
        <span class="scanner-corner corner-bl"></span>
        <span class="scanner-corner corner-br"></span>

        <div class="scanner-chip">AI</div>
        <div class="scanner-line"></div>
        <span class="scanner-caption">OBJECT DETECTION</span>
      </div>
    </div>

    <div class="visual-tag tag-model">YOLO · COMPUTER VISION</div>
    <div class="visual-tag tag-device">
      <span class="brand-status"></span>
      On-device camera
    </div>
  </div>
</section>

<section class="home-section">
  <div class="section-heading">
    <div>
      <div class="eyebrow">THE PLATFORM</div>
      <h2>Waste identification, simplified.</h2>
      <p>One system to capture, detect, and review electronic waste.</p>
    </div>
  </div>

  <div class="feature-grid">
    <article class="feature-card">
      <div class="feature-icon">◎</div>
      <span class="feature-number">01</span>
      <h3>Capture</h3>
      <p>
        Use the connected Raspberry Pi camera to view an electronic
        waste item before analysis.
      </p>
    </article>

    <article class="feature-card">
      <div class="feature-icon">◈</div>
      <span class="feature-number">02</span>
      <h3>Identify</h3>
      <p>
        Run YOLO object detection through the FastAPI backend to
        identify objects in the captured image.
      </p>
    </article>

    <article class="feature-card">
      <div class="feature-icon">⌁</div>
      <span class="feature-number">03</span>
      <h3>Review results</h3>
      <p>
        Review detected object names, confidence scores, and
        bounding-box coordinates.
      </p>
    </article>
  </div>
</section>

<section class="home-cta">
  <div>
    <div class="eyebrow">READY TO BEGIN?</div>
    <h2>Start an EcoSort scan.</h2>
    <p>Position an item in front of the camera and analyze it.</p>
  </div>

  <button
    class="primary-button"
    onclick={() => onNavigate('/analyze')}
  >
    Open Analyzer <span aria-hidden="true">→</span>
  </button>
</section>