import { logger } from "../../../core/logging";
export class BaseGLGlyph {
    constructor(gl, glyph) {
        this.gl = gl;
        this.glyph = glyph;
        this.nvertices = 0;
        this.size_changed = false;
        this.data_changed = false;
        this.visuals_changed = false;
        this.init();
    }
    set_data_changed() {
        const { data_size } = this.glyph;
        if (data_size != this.nvertices) {
            this.nvertices = data_size;
            this.size_changed = true;
        }
        this.data_changed = true;
    }
    set_visuals_changed() {
        this.visuals_changed = true;
    }
    render(_ctx, indices, mainglyph) {
        if (indices.length == 0) {
            // Implementations assume at least one index to draw. We return true,
            // because there is no need to switch back to a fallback renderer.
            return true;
        }
        // Get transform
        const [a, b, c] = [0, 1, 2];
        let wx = 1; // Weights to scale our vectors
        let wy = 1;
        let [dx, dy] = this.glyph.renderer.coordinates.map_to_screen([a * wx, b * wx, c * wx], [a * wy, b * wy, c * wy]);
        if (isNaN(dx[0] + dx[1] + dx[2] + dy[0] + dy[1] + dy[2])) {
            logger.warn(`WebGL backend (${this.glyph.model.type}): falling back to canvas rendering`);
            return false;
        }
        // Try again, but with weighs so we're looking at ~100 in screen coordinates
        wx = 100 / Math.min(Math.max(Math.abs(dx[1] - dx[0]), 1e-12), 1e12);
        wy = 100 / Math.min(Math.max(Math.abs(dy[1] - dy[0]), 1e-12), 1e12);
        [dx, dy] = this.glyph.renderer.coordinates.map_to_screen([a * wx, b * wx, c * wx], [a * wy, b * wy, c * wy]);
        // Test how linear it is
        if ((Math.abs((dx[1] - dx[0]) - (dx[2] - dx[1])) > 1e-4) ||
            (Math.abs((dy[1] - dy[0]) - (dy[2] - dy[1])) > 1e-4)) {
            logger.warn(`WebGL backend (${this.glyph.model.type}): falling back to canvas rendering`);
            return false;
        }
        const [sx, sy] = [(dx[1] - dx[0]) / wx, (dy[1] - dy[0]) / wy];
        const { width, height } = this.glyph.renderer.plot_view.canvas_view.webgl.canvas;
        const trans = {
            pixel_ratio: this.glyph.renderer.plot_view.canvas_view.pixel_ratio,
            width, height,
            dx: dx[0] / sx, dy: dy[0] / sy, sx, sy,
        };
        this.draw(indices, mainglyph, trans);
        return true;
    }
}
BaseGLGlyph.__name__ = "BaseGLGlyph";
//# sourceMappingURL=base.js.map