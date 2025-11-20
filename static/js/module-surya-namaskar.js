/**
 * Surya Namaskar Module JavaScript
 * Handles image loading with fallback mechanism and performance monitoring
 */

(function() {
    'use strict';

    const P = window.performance;
    const M = { i: [], m: {} };

    /**
     * Mark a performance milestone
     * @param {string} n - Name of the milestone
     */
    function mark(n) {
        if (P && P.mark) {
            P.mark(n);
            M.m[n] = P.now();
            console.log(`[Perf] ${n}: ${M.m[n].toFixed(2)}ms`);
        }
    }

    /**
     * Track image load performance
     * @param {string} s - Image source URL
     * @param {number} t - Load time in milliseconds
     * @param {number} ok - Success flag (1 = success, 0 = failure)
     */
    function track(s, t, ok) {
        M.i.push({ s, t, ok, ts: Date.now() });
        console.log(`[Perf] Image ${ok ? 'OK' : 'FAIL'}: ${s} (${t.toFixed(2)}ms)`);
    }

    // Mark page start
    mark('page-start');

    // Initialize image loading handlers when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        mark('dom-ready');

        const imgs = document.querySelectorAll('.pose-image');

        imgs.forEach(function(img) {
            const t0 = P.now();
            const src = img.src;

            // Handle successful image load
            img.addEventListener('load', function() {
                track(src, P.now() - t0, 1);
            });

            // Handle image load error with fallback mechanism
            img.addEventListener('error', function() {
                track(src, P.now() - t0, 0);

                // First retry: try alternative image path
                if (!this.hasAttribute('data-retry')) {
                    this.setAttribute('data-retry', '1');
                    this.src = src.replace('/src/', '/').replace('.jpg', '-removebg-preview.png');
                } else {
                    // Final fallback: display placeholder
                    const c = this.parentElement;
                    const a = this.alt || '';
                    const n = a.match(/\d+/)?.[0] || '';
                    const p = a.split('-')[0].trim() || 'Pose';

                    c.innerHTML = `
                        <div style="text-align:center;color:#64748b;padding:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;width:100%">
                            <div style="font-size:4rem;margin-bottom:15px;opacity:.6">🧘</div>
                            <p style="font-size:16px;font-weight:600;margin:0;color:#475569">${p}</p>
                            ${n ? `<p style="font-size:14px;margin:5px 0;color:#64748b">Step ${n}</p>` : ''}
                            <p style="font-size:12px;margin:10px 0 0;opacity:.7;color:#94a3b8">Image unavailable</p>
                        </div>
                    `;
                }
            });
        });
    });

    // Track page load completion and calculate metrics
    window.addEventListener('load', function() {
        mark('page-loaded');

        // Measure performance metrics
        if (P && P.measure) {
            try {
                P.measure('dom-time', 'page-start', 'dom-ready');
                P.measure('load-time', 'page-start', 'page-loaded');
            } catch (e) {
                // Ignore measurement errors
            }
        }

        // Log image loading summary after a short delay
        setTimeout(function() {
            const ok = M.i.filter(x => x.ok);
            const fail = M.i.filter(x => !x.ok);

            if (ok.length) {
                const avg = ok.reduce((s, x) => s + x.t, 0) / ok.length;
                console.log(`[Perf] Images: ${ok.length} loaded (avg ${avg.toFixed(2)}ms), ${fail.length} failed`);
            }
        }, 1000);
    });
})();
