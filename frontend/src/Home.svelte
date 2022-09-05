<script lang="ts">
    import { useSWR } from "sswr";
    import { CheckIcon } from "svelte-feather-icons";
    import { formatEnd } from "./utils";
  
    const { data: people, revalidate } = useSWR("https://gongy-93-fastapi.modal.run/home");

    $: console.log($people);
  </script>
  
{#if $people}
  <div class="grid grid-cols-1 xs:grid-cols-2 sm:grid-cols-3">
      {#each $people.splice(1) as person}
        <div class="flex items-center bg-gray-600 text-zinc-100 p-2 rounded-md my-1 mx-1">
          <div class="w-2 h-2 bg-green-600 rounded-lg mr-4 ml-2"/>
          {person}
        </div>
      {/each}
  </div>
  <div class="m-1 mt-4 text-zinc-100 text-center">
    Updated {formatEnd($people[0] * 1000)} ago.
  </div>
{/if}