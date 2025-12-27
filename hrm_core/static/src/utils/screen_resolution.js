/** @odoo-module */

export function getScreenResolution() {
    const realWidth = window.screen.width * window.devicePixelRatio;
    const realHeight = window.screen.height * window.devicePixelRatio;
    return {width: realWidth, height: realHeight};
}

export function isLandscape() {
    const {width, height} = getScreenResolution();
    return width > height;
}