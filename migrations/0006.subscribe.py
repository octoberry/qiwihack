step(
    """
    CREATE SEQUENCE subscribe_id_seq;
    CREATE TABLE subscribe (
        "id" int4 NOT NULL DEFAULT nextval('subscribe_id_seq'),
        "email" varchar(255) NOT NULL,
        "tags" varchar(255) NOT NULL,
        "created_at" timestamp(6) NOT NULL default CURRENT_TIMESTAMP,
        "updated_at" timestamp(6) NOT NULL default CURRENT_TIMESTAMP,
        CONSTRAINT "subscribe_pkey" PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE
    )
    WITH (OIDS=FALSE);
    ALTER SEQUENCE subscribe_id_seq OWNED BY subscribe.id;
    """
)
