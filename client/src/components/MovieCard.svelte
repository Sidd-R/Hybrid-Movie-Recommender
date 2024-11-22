<script lang="ts">
	import { ApiClient } from "../models";
	let heart = false;
	let thumbnail: string = ''; // Thumbnail URL placeholder.

	interface Movie {
		movieId: number;
		title: string;
		recommended_from: string;
	}

	export let movie: Movie;

	// Your OMDb API Key
	const OMDB_API_KEY = 'f025fe6d';

	// Fetch thumbnail from OMDb API
	const fetchThumbnail = async () => {
		console.log('Fetching thumbnail for movie:', movie.title);

		try {
			// Extract year and clean title
			const year = movie.title.match(/\((\d{4})\)/)?.[1]; // Extract the year
			const cleanTitle = movie.title
				.replace(/\s*\([^)]*\)/g, '') // Remove year and parentheses
				.replace(/,\s*(The|A|An)$/i, ''); // Handle ", The" or similar

			// Build the API URL
			const url = `https://www.omdbapi.com/?apikey=${OMDB_API_KEY}&t=${encodeURIComponent(cleanTitle)}${year ? `&y=${year}` : ''}`;
			console.log('OMDb API URL:', url);

			// Fetch data
			const response = await fetch(url);
			const data = await response.json();

			console.log('API Response:', data);

			if (data && data.Poster && data.Poster !== 'N/A') {
				thumbnail = data.Poster;
			} else {
				console.warn('No poster found for this movie:', movie.title);
				thumbnail = 'https://via.placeholder.com/500x750?text=No+Image';
			}
		} catch (error) {
			console.error('Failed to fetch movie thumbnail:', error);
			thumbnail = 'https://via.placeholder.com/500x750?text=Error';
		}
	};

	// Fetch the thumbnail on component load
	fetchThumbnail();

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

<div class="group relative">
	<div class="absolute top-4 right-4 bg-gray-300 px-2 py-1 rounded-full text-xs">
		{movie.recommended_from}
	</div>
	<img
		src={thumbnail}
		alt={movie.title}
		class="w-full rounded-lg bg-gray-200 object-fill group-hover:opacity-75 xl:aspect-[6/8]"
	/>
	<div class="flex justify-between px-4 py-2">
		<h3 class="mt-4 text-sm text-gray-700">{movie.title}</h3>
		<button onclick={handleLikeToggle} aria-label="heart button">
			<p class="mt-2 text-lg font-medium text-gray-900">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill={heart ? '#ff5245' : 'none'}
					viewBox="0 0 24 24"
					stroke-width={heart ? '0' : '1.5'}
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
