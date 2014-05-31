step(
    """CREATE SEQUENCE events_id_seq;
    CREATE TABLE events (
        "id" int4 NOT NULL DEFAULT nextval('events_id_seq'),
        "description" text NOT NULL,
        "amount" int4 NOT NULL,
        "card" varchar(255) NOT NULL,
        "image" varchar(255) NOT NULL,
        "created_at" timestamp(6) NOT NULL,
        "updated_at" timestamp(6) NOT NULL,
        CONSTRAINT "events_pkey" PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE
    )
    WITH (OIDS=FALSE);
    ALTER SEQUENCE events_id_seq OWNED BY events.id;
    """
)
