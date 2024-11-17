<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import axios from 'axios';
  import Cookies from 'js-cookie';
	let email = '';
	let password = '';
	let currentData: 'EMAIL' | 'PROFILE' = 'EMAIL';
	let prefrences: string[] = [];
	onMount(() => {});

	const handlePrefrences = (event: any) => {
		console.log('event.target.value', event.target.value);
		console.log('event.target.checked', event.target.checked);
		if (event.target.checked) {
			prefrences.push(event.target.name);
		} else {
			prefrences = prefrences.filter((pref) => pref !== event.target.name);
		}
		console.log('prefrences', prefrences);
	};

	const handleSubmit = async (event: any) => {
		event.preventDefault();
		try {
      await axios.post('http://127.0.0.1:8000/api/auth/register/', {
        email,
        password,
        prefrences
      }).then(res => {
        Cookies.set('token', res.data.access);
        Cookies.set('refresh_token', res.data.refresh)
      })

			window.location.replace('http://localhost:5173')

		} catch (error) {
			// addToast(error.message, 'error');
      alert(error)
		}
	};

</script>

{#if currentData === 'EMAIL'}
	<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
		<div class="sm:mx-auto sm:w-full sm:max-w-sm">
			<img
				class="mx-auto h-10 w-auto"
				src="https://tailwindui.com/plus/img/logos/mark.svg?color=indigo&shade=600"
				alt="Your Company"
			/>
			<h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">
				Create a new account
			</h2>
		</div>

		<div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
			<form class="space-y-6" action="#" method="POST">
				<div>
					<label for="email" class="block text-sm/6 font-medium text-gray-900">Email address</label>
					<div class="mt-2">
						<input
							id="email"
							name="email"
							type="email"
							autocomplete="email"
							required
							class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
							value={email}
							onchange={(e) => (email = (e.target as HTMLInputElement).value)}
						/>
					</div>
				</div>

				<div>
					<div class="flex items-center justify-between">
						<label for="password" class="block text-sm/6 font-medium text-gray-900">Password</label>
					</div>
					<div class="mt-2">
						<input
							id="password"
							name="password"
							type="password"
							autocomplete="current-password"
							required
							class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
							value={password}
							onchange={(e) => (password = (e.target as HTMLInputElement).value)}
						/>
					</div>
				</div>

				<div>
					<button
						onclick={() => {
              currentData = 'PROFILE';
            }}
						class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
						>Continue</button
					>
				</div>
			</form>
		</div>
	</div>
{/if}

{#if currentData === 'PROFILE'}
	<form class="px-32 py-20">
		<div class="space-y-12">
			<div class="border-b border-gray-900/10 pb-12">
				<h2 class="text-base/7 font-semibold text-gray-900">Profile</h2>
				<p class="mt-1 text-sm/6 text-gray-600">
					Choose your favorite genres so we can show you the most relevant content.
				</p>

				<div class="border-b border-gray-900/10 pb-12">
					<div class="mt-10 space-y-10">
						<fieldset>
							<legend class="text-sm/6 font-semibold text-gray-900">Genres</legend>
							<div class="mt-6 space-y-6">
								<div class="relative flex gap-x-3">
									<div class="flex h-6 items-center">
										<!-- ['Action',
 'Adventure',
 'Animation',
 'Children',
 'Comedy',
 'Crime',
 'Documentary',
 'Drama',
 'Fantasy',
 'Film-Noir',
 'Horror',
 'IMAX',
 'Musical',
 'Mystery',
 'Romance',
 'Sci-Fi',
 'Thriller',
 'War',
 'Western'] -->
										<input
											id="Action"
											name="Action"
											type="checkbox"
											class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"
                      onchange="{handlePrefrences}"
										/>
									</div>
									<div class="text-sm/6">
										<label for="comments" class="font-medium text-gray-900">Action</label>
									</div>
								</div>
								<div class="relative flex gap-x-3">
									<div class="flex h-6 items-center">
										<input
											id="Adventure"
											name="Adventure"
											type="checkbox"
											class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"
                      onchange="{handlePrefrences}"
										/>
									</div>
									<div class="text-sm/6">
										<label for="comments" class="font-medium text-gray-900">Adventure</label>
									</div>
								</div>
								<div class="relative flex gap-x-3">
									<div class="flex h-6 items-center">
										<input
											id="Animation"
											name="Animation"
											type="checkbox"
											class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"
                      onchange="{handlePrefrences}"
										/>
									</div>
									<div class="text-sm/6">
										<label for="comments" class="font-medium text-gray-900">Animation</label>
									</div>
								</div>
								<div class="relative flex gap-x-3">
									<div class="flex h-6 items-center">
										<input
											id="Children"
											name="Children"
											type="checkbox"
											class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"
                      onchange="{handlePrefrences}"
										/>
									</div>
									<div class="text-sm/6">
										<label for="comments" class="font-medium text-gray-900">Children</label>
									</div>
								</div>
								<div class="relative flex gap-x-3">
									<div class="flex h-6 items-center">
										<input
											id="Comedy"
											name="Comedy"
											type="checkbox"
											class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"
                      onchange="{handlePrefrences}"
										/>
									</div>
									<div class="text-sm/6">
										<label for="comments" class="font-medium text-gray-900">Comedy</label>
									</div>
								</div>
							</div>
						</fieldset>
					</div>
				</div>
			</div>

			<div class="mt-6 flex items-center justify-end gap-x-6">
				<button type="button" class="text-sm/6 font-semibold text-gray-900">Cancel</button>
				<button
					type="submit"
					class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          onclick="{handleSubmit}"
					>Save</button
				>
			</div>
		</div>
	</form>
{/if}
