<script lang="ts">
    import { useSWR } from "sswr";
    import { WifiIcon } from "svelte-feather-icons";
  
    const { data: people, revalidate } = useSWR("https://gongy-93-fastapi.modal.run/home");

    $: console.log($people);
  </script>
  
    <div class="grid grid-cols-1 xs:grid-cols-2 sm:grid-cols-3">
      {#if $people}
        {#each $people as person}
          <div class="flex items-center bg-gray-600 text-zinc-100 p-2 rounded-md my-1 mx-1">
            <WifiIcon class="w-4 h-4 text-green-600 mr-4 ml-2"/>
            {person}
          </div>
        {/each}
      {/if}
    </div>
  <div class="m-1 p-2 rounded-md text-zinc-100 text-left">
    Updated 
  </div>