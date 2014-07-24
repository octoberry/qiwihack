step(
    """
    CREATE SEQUENCE transaction_id_seq;
    CREATE TABLE transaction (
        "id" int4 NOT NULL DEFAULT nextval('transaction_id_seq'),
        "event_id" int4 NOT NULL,
        "amount" int4 NOT NULL,
        "card" varchar(255) NOT NULL,
        "md" varchar(255) NOT NULL,
        "status" int4 NOT NULL DEFAULT 0,
        "created_at" timestamp(6) NOT NULL,
        "updated_at" timestamp(6) NOT NULL,
        CONSTRAINT "transaction_pkey" PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE
    )
    WITH (OIDS=FALSE);
    ALTER SEQUENCE transaction_id_seq OWNED BY transaction.id;
    ALTER TABLE transaction ADD CONSTRAINT transaction_event_id_fkey FOREIGN KEY(event_id) REFERENCES events(id) on delete cascade;
    CREATE UNIQUE INDEX "transaction_md_key" ON transaction (md);
    CREATE INDEX "transaction_status_key" ON transaction (status);
    """
)
