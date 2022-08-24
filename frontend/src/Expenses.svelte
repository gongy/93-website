<script lang="ts">
  import clsx from "clsx";
  import { useSWR } from "sswr";

  import {
    LoaderIcon,
    TrashIcon,
  } from "svelte-feather-icons";

  const { data: rows, revalidate } = useSWR("https://gongy-93-fastapi.modal.run/expenses");

  function openNewTab(url: string) {
    window.open(url, "_blank");
  }
</script>

<div class="m-1 p-2 bg-gray-600 rounded-md">
{#if $rows}
    {#each $rows as row, i (i)}
    <div class="first:text-zinc-300 border-b last:border-b-0 first:pt-0 last:pb-0 p-2 grid grid-cols-9 text-zinc-100 border-gray-500">
        <div class="col-span-2 truncate">{row[0]}</div>
        <div class="col-span-4 text-ellipsis">{row[1]}</div>
        <div class="col-span-2 truncate">{row[3]}</div>
        {#if i == 0}
        <div class="col-span-1 text-wrap"></div>
        {:else}
        <div class="col-span-1 text-wrap bg-gray-400 hover:bg-red-500 w-6 h-6 m-auto p-1.5 rounded-lg">
            <TrashIcon class="w-3 h-3"/>
        </div>
        {/if}
    </div>
    {/each}
{:else}
    <div class="h-7 animate-pulse bg-gray-400 rounded-sm my-2 mx-1"/>
    <div class="h-7 animate-pulse bg-gray-400 rounded-sm my-2 mx-1"/>
{/if}
</div>
<div class="flex justify-items-stretch">
    <button
        on:click={() => {
            openNewTab(
                "https://docs.google.com/spreadsheets/d/1988nYIzBAVzhjlSWTuJ___uQb610KfLLpGZh-xvpd2M/edit#gid=0"
            );
        }}
        class={clsx(
            "h-10 m-1 p-2 text-zinc-100 rounded-md bg-gray-600 hover:bg-gray-500 grow"
        )}
    >
        +
    </button>
</div>