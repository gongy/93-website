<script lang="ts">
  import clsx from "clsx";
  import Expenses from "./Expenses.svelte";
  import Laundry from "./Laundry.svelte";
  import Button from "./Button.svelte";
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
</script>

<main>
  <h1 class="text-center pt-10 pb-8 text-zinc-100 text-3xl font-light">
    93 Leonard
  </h1>
  <div class="grid grid-cols-1 2xs:grid-cols-2 sm:grid-cols-4 pb-3">
    {#each options as option (option)}
      <Button
        selectedClass="bg-slate-900 ring-slate-900"
        selected={selected === option.name}
        on:click={() => {
          selected = option.name;
        }}
      >
        <div class="flex align-center justify-center">
          <svelte:component
            this={option.icon}
            class="flex-shrink-0 w-5 h-5 mx-1 mt-0.5"
          />
          <div class="mx-1">{option.name}</div>
        </div>
      </Button>
    {/each}
  </div>
  <div>
    {#if selected == "Expenses"}
      <Expenses/>
    {:else if selected == "Laundry"}
      <Laundry/>
    {/if}
  </div>
</main>
