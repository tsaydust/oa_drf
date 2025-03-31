import login from "@/views/login/login.vue"
import githubCallback from "@/views/login/github-callback.vue"

const routes = [
    {
        path: "/login",
        name: "login",
        component: login,
    },
    {
        path: "/oaauth/github/callback",
        name: "github-callback",
        component: githubCallback,
    },
];

export default routes;
