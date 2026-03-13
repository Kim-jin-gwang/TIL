import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MovieListView from '../views/MovieListView.vue'
import MovieDetailView from '../views/MovieDetailView.vue'
import ReviewSearchView from '../views/ReviewSearchView.vue'
import RecommendedView from '../views/RecommendedView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/',               component: HomeView },
    { path: '/movies',         component: MovieListView },
    { path: '/:movieId',       component: MovieDetailView },
    { path: '/review-search',  component: ReviewSearchView },
    { path: '/recommended',    component: RecommendedView },
  ],
})

export default router