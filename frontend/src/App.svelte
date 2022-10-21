<script lang="ts">
  import clsx from "clsx";;
  import Expenses from "./Expenses.svelte";
  import Laundry from "./Laundry.svelte";
  import Home from "./Home.svelte";
  import Games from "./Games.svelte";
  import Button from "./Button.svelte";
  import {
    CreditCardIcon,
    HomeIcon,
    SpeakerIcon,
    ZapIcon,
  } from "svelte-feather-icons";
  import { userToken } from "./stores";

  import jwt_decode from "jwt-decode";

  const options = [
    { name: "Home", icon: HomeIcon },
    { name: "Laundry", icon: SpeakerIcon },
    { name: "Expenses", icon: CreditCardIcon },
    { name: "Games", icon: ZapIcon },
  ];

  let selected: string = options[0].name;
  let card: any;

  let user: any;
  let hoveringBubble = false;

  (window as any).handleCredentialResponse = (response: any) => {
    userToken.set(response.credential as string);
  }

  $: if ($userToken) {
    user = jwt_decode($userToken);
    console.log("ID: " + user.sub);
    console.log('Full Name: ' + user.name);
    console.log('Given Name: ' + user.given_name);
    console.log('Family Name: ' + user.family_name);
    console.log("Image URL: " + user.picture);
    console.log("Email: " + user.email);
  }
</script>

<svelte:head>
  <script src="https://accounts.google.com/gsi/client" async defer></script>
</svelte:head>

<main>
  <h1 class="grid grid-cols-3 pt-10 pb-8">
    <div class="col-start-2 col-span-1 text-center mx-auto text-zinc-100 text-3xl font-light">
      93 Leonard
    </div>
    {#if user}
    <div class="flex items-center justify-end">
      <img
        on:click={() => {
          console.log("HI");
          userToken.set("");
          user = undefined;
        }}
        class="rounded-full w-8 h-8 my-auto mx-1 cursor-pointer"
        src={user.picture}
        alt={user.name}
      />
      </div>
    {/if}
  </h1>

  <div class="grid grid-cols-1 2xs:grid-cols-2 sm:grid-cols-4 pb-3">
    {#each options as option (option)}
      <Button
        selectedClass="bg-gray-700 ring-gray-700"
        selected={selected === option.name}
        on:click={() => {
          selected = option.name;
        }}
      >
        <div class="flex align-center justify-center">
          <svelte:component
            this={option.icon}
            bind:this={card}
            class="flex-shrink-0 w-5 h-5 mx-1 mt-0.5"
          />
          <div class="mx-1">{option.name}</div>
        </div>
      </Button>
    {/each}
  </div>

    <div class={clsx(
      "flex justify-center pt-5",
      user ? "hidden" : "")}
    >
      <div id="g_id_onload"
        data-client_id="971159492117-cc6jhib74lf8egu0cm67v73jr20k4vvt.apps.googleusercontent.com"
        data-callback="handleCredentialResponse"
        data-auto_prompt="false">
      </div>
      <div class="g_id_signin"
        data-type="standard"
        data-size="large"
        data-theme="filled_black"
        data-text="signin"
        data-shape="rectangular"
        data-logo_alignment="left">
      </div>
    </div>
  {#if user}
    <div>
      {#if selected == "Expenses"}
        <Expenses/>
      {:else if selected == "Laundry"}
        <Laundry/>
      {:else if selected == "Home"}
        <Home/>
      {:else if selected == "Games"}
        <Games/>
      {/if}
    </div>
  {/if}
</main>
