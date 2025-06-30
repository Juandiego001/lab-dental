<template>
<v-container fluid class="fill-height justify-center">
    Página de recuperación de contraseña
    <template :key="`${i}category`" v-for="category, i  in categories">
        <p class="text-h2">{{ category.name }}</p>
        <div v-for="movies, i in category.movies">
            {{  movies.trailerVideo  }}
            <video v-if="movies.trailerVideo" :src="`http://localhost:5000/api/${movies.trailerVideo}`">
            </video>
        </div>
    </template>
</v-container>
</template>

<script>

export default {
    data: () => ({
      test: '1' ,
      categories: [],
      movies: []
    }),
    async beforeMount () {
        const { items } = await $api('/api/categories/', {
            query: {
                search: '',
                page: 1,
                perPage: 15
            }
        })
        this.categories = items
    },
    watch: {
        async categories (val) {
            for (const category of val) {
                category.movies = await this.getMovies(category.id)
            }
        }
    },
    methods: {
        async getMovies(categoryId) {
            try {
                const { items } = await $api(`/api/movies/category/${categoryId}`, {
                    query: {
                        search: '',
                        page: 1,
                        perPage: 15
                    }
                })
                return items
            } catch (err ) {
                console.log(err)
            }
        }
    }
}
</script>
