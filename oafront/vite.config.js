import {fileURLToPath, URL} from 'node:url'

import {defineConfig, loadEnv} from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'
import VueSetupExtend from 'vite-plugin-vue-setup-extend'
import {createHtmlPlugin} from "vite-plugin-html";
// https://vitejs.dev/config/

const getViteEnv = (mode, target) => {
    return loadEnv(mode, process.cwd())[target];
};

export default ({mode}) => {
    return defineConfig({
        plugins: [
            vue(),
            VueDevTools(),
            VueSetupExtend(),
            createHtmlPlugin({
                inject: {
                    data: {
                        title: getViteEnv(mode, "VITE_APP_TITLE"),
                    },
                },
            }),
        ],
        resolve: {
            alias: {
                '@': fileURLToPath(new URL('./src', import.meta.url))
            }
        }
    })
}
