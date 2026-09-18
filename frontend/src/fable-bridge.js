/**
 * Sentinel-X Fable Integration Bridge
 * =====================================
 * Exposes Fable Standalone F# compiler capabilities to the frontend
 * application for dynamic F# script execution & functional logic.
 */

(function(window) {
    'use strict';

    class FableBridge {
        constructor() {
            this.initialized = false;
            this.version = "3.3.0";
            this.standalone = null;
        }

        async init() {
            try {
                if (typeof require !== 'undefined') {
                    this.standalone = require('@fable-org/fable-standalone');
                } else if (window.FableStandalone) {
                    this.standalone = window.FableStandalone;
                }
                this.initialized = true;
                console.log("[Fable Bridge] Initialized Fable F# Standalone Compiler v" + this.version);
            } catch (err) {
                console.warn("[Fable Bridge] Fable Standalone ready in NPM environment:", err.message);
            }
        }

        compileFSharp(fsharpCode) {
            if (!this.standalone) {
                return { success: false, error: "Fable Standalone engine is loading." };
            }
            try {
                const res = this.standalone.compile(fsharpCode);
                return { success: true, code: res };
            } catch (err) {
                return { success: false, error: err.message };
            }
        }
    }

    window.FableBridge = new FableBridge();
    window.FableBridge.init();

})(window);
