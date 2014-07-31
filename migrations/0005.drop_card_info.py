step(
    """
    ALTER TABLE events ADD COLUMN rebill_anchor varchar(255);
    ALTER TABLE events DROP COLUMN card;
    ALTER TABLE "transaction" DROP COLUMN card;
    """
)