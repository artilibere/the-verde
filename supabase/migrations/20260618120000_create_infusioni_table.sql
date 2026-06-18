-- Diario tè: infusioni sincronizzate per utente (auth anonima o registrata)

create table public.infusioni (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  client_id bigint not null,
  varieta text not null,
  temp smallint,
  grams numeric(5, 2),
  seconds smallint,
  note text not null default '',
  tags text[] not null default '{}',
  momento text,
  season text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (user_id, client_id)
);

create index infusioni_user_id_created_at_idx
  on public.infusioni (user_id, created_at desc);

create or replace function public.set_infusioni_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger infusioni_updated_at
  before update on public.infusioni
  for each row
  execute function public.set_infusioni_updated_at();

alter table public.infusioni enable row level security;

create policy "infusioni_select_own"
  on public.infusioni
  for select
  to authenticated
  using (auth.uid() = user_id);

create policy "infusioni_insert_own"
  on public.infusioni
  for insert
  to authenticated
  with check (auth.uid() = user_id);

create policy "infusioni_update_own"
  on public.infusioni
  for update
  to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "infusioni_delete_own"
  on public.infusioni
  for delete
  to authenticated
  using (auth.uid() = user_id);
