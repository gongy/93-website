<script lang="ts">
  import { useSWR } from "sswr";
  import PersonSelection from "./PersonSelection.svelte";

  const { data, revalidate } = useSWR("https://gongy-93-fastapi.modal.run/elo");

  const people = ["ak", "dansun", "cjs", "rgong", "jlee", "bwu"];

  let winner = "";
  let loser = "";

  async function sendGameUpdate (winner, loser) {
    console.log("game", winner, loser);
    const res = await fetch('https://gongy-93-fastapi.modal.run/game', {
          method: "POST",
          headers: {
              "Content-type": "application/json"
          },
          body: JSON.stringify({ winner, loser })
      });
  }
</script>

<div class="grid grid-cols-1 2xs:grid-cols-2 xs:grid-cols-3 sm:grid-cols-6 p-2 m-1 rounded-md bg-gray-600">
  {#each people as person}
    <div class="flex flex-col text-center">
      <div class="text-zinc-100">{person}</div>
      <div class="text-zinc-400">1500</div>
    </div>
  {/each}
</div>

<div class="rounded-md grid grid-cols-2">
  <div class="flex flex-col bg-gray-600 m-1 p-2 rounded-md">
    <div class="text-zinc-100 text-center">Winner</div>
    <PersonSelection bind:selected={winner} clz="flex flex-col"/>
  </div>
  <div class="flex flex-col bg-gray-600 m-1 p-2 rounded-md">
    <div class="text-zinc-100 text-center">Loser</div>
    <PersonSelection bind:selected={loser} clz="flex flex-col"/>
  </div>
  <div class="flex flex-col col-span-2 bg-gray-600 m-1 p-2 rounded-md hover:bg-gray-500 active:bg-gray-700 cursor-pointer">
    <div on:click={() => {sendGameUpdate(winner, loser);}} class="text-zinc-100 text-center">Submit</div>
  </div>
</div>
