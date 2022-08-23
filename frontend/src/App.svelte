<script lang="ts">
  import clsx from "clsx";
  import { useSWR } from "sswr";
  import {
    BoxIcon,
    CreditCardIcon,
    SpeakerIcon,
    UserIcon,
  } from "svelte-feather-icons";

  const options = [
    { name: "Expenses", icon: CreditCardIcon },
    { name: "Laundry", icon: SpeakerIcon },
    { name: "Guests", icon: UserIcon },
    { name: "Packages", icon: BoxIcon },
  ];

  let selected: string = "Expenses";

  function openNewTab(url: string) {
    window.open(url, "_blank");
  }

  const { data: rows, revalidate } = useSWR("https://gongy-93-fastapi.modal.run/expenses");

  $: if ($rows) console.log($rows);
</script>

<main>
  <h1 class="text-center pt-10 pb-5 text-zinc-100 text-3xl font-light">
    93 Leonard
  </h1>
  <div class="grid grid-cols-1 xs:grid-cols-2 sm:grid-cols-4">
    {#each options as option (option)}
      <button
        on:click={() => {
          selected = option.name;
        }}
        class={clsx(
          "m-1 p-2 text-zinc-100 rounded-md ring-1 hover:ring-gray-400",
          selected == option.name
            ? "ring-gray-500 bg-gray-500 text-zinc-100"
            : "ring-gray-600 bg-gray-600 text-zinc-200"
        )}
      >
        <div class="flex align-center justify-center">
          <svelte:component
            this={option.icon}
            class="flex-shrink-0 w-5 h-5 mx-1 mt-0.5"
          />
          <div class="mx-1">{option.name}</div>
        </div>
      </button>
    {/each}
  </div>
  <div>
    {#if selected == "Expenses"}
      {#if $rows}
        <div class="m-1 p-2 bg-gray-600 rounded-md">
          {#each $rows as row, i (i)}
            <div class="first:text-zinc-300 border-b last:border-b-0 first:pt-0 last:pb-0 p-2 grid grid-cols-6 text-zinc-100 border-gray-500">
              <div class="col-span-1 text-wrap">{row[0]}</div>
              <div class="col-span-2 text-wrap">{row[1]}</div>
              <div class="col-span-2 text-wrap">{row[2]}</div>
              <div class="col-span-1 text-wrap">{row[3]}</div>
            </div>
          {/each}
        </div>
      {/if}
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
          Go
        </button>
      </div>
    {/if}
  </div>
</main>
