<script lang="ts">
    import { useSWR } from "sswr";
    import { utcTs, formatEnd } from "./utils";
  
    const { data: people, revalidate } = useSWR("https://gongy-93-fastapi.modal.run/home");

    function minsAgo (t) {
      return Math.floor((utcTs() / 1000 - t) / 60);
    }

    $: console.log($people);
  </script>
  
{#if $people}
  <div class="grid grid-cols-1 xs:grid-cols-2 sm:grid-cols-3">
      {#each $people.filter((p: any) => p.name != "updated_at") as person}
        <div class="flex items-center bg-gray-600 text-zinc-100 p-1 px-3 rounded-md my-1 mx-1">
          {#if minsAgo(person.time) < 5}
            <div class="shrink-0 w-2 h-2 bg-green-600 rounded-lg mr-3"/>
          {:else if minsAgo(person.time) < 15}
            <div class="shrink-0 w-2 h-2 bg-orange-600 rounded-lg mr-3"/>
          {:else}
            <div class="shrink-0 w-2 h-2 bg-red-600 rounded-lg mr-3"/>
          {/if}
          {person.name}
          {#if minsAgo(person.time) >= 5}
            <span class="ml-auto text-zinc-400">
              {minsAgo(person.time)}m
            </span>
          {/if}
        </div>
      {/each}
  </div>
  <div class="m-1 mt-4 text-zinc-100 text-center">
    Updated {formatEnd(($people.find((p: any) => p.name == "updated_at")?.time ?? 0) * 1000)} ago.
  </div>
{/if}