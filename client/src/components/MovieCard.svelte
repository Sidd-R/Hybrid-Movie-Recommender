<script lang="ts">
	import { ApiClient } from "../models";

	
	interface Movie {
		movieId: number;
		title: string;
		recommended_from: string;
	}
	export let movie:Movie;
	let heart = false;

	const handleLikeToggle = () => {
		if (!heart) {
			ApiClient.get('/movies/like/?movie_id='+movie.movieId);
			heart = true;
		} else {
			heart = false;
			ApiClient.get('/movies/unlike/?movie_id='+movie.movieId);
		}
	}
</script>

<div class="group relative" >
	<div class="absolute top-4 right-4 bg-gray-300 px-2 py-1 rounded-full text-xs">
		{movie.recommended_from}
	</div>
	<img
		src="https://image.tmdb.org/t/p/original/j9hcMf4ZSf8fGlUbKNTASUmp3SX.jpg"
		alt="Tall slender porcelain bottle with natural clay textured body and cork stopper."
		class=" w-full rounded-lg bg-gray-200 object-fill group-hover:opacity-75 xl:aspect-[6/8]"
	/>
	<div class="flex justify-between px-4 py-2">
		<h3 class="mt-4 text-sm text-gray-700">{movie.title}</h3>
		<button onclick={handleLikeToggle} aria-label="heart button">
				<p class="mt-2 text-lg font-medium text-gray-900">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill={heart?'#ff5245':'none'}
				viewBox="0 0 24 24"
				stroke-width={heart?'0':'1.5'}
				stroke="currentColor"
				class="size-6"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z"
				/>
			</svg>
		</p>
		</button>
	</div>
</div>
