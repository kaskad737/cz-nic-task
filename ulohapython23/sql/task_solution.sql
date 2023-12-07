CREATE TABLE IF NOT EXISTS domain (
    domain_name TEXT PRIMARY KEY NOT NULL,
    expired BOOLEAN DEFAULT false,
    outzone BOOLEAN DEFAULT false,
    delete_candidate BOOLEAN DEFAULT false,
    datetime_registration TIMESTAMPTZ DEFAULT now(),
    datetime_unregistration TIMESTAMPTZ
    );

CREATE TABLE IF NOT EXISTS domain_flag (
    domain_name TEXT NOT NULL REFERENCES domain(domain_name),
    flag_name TEXT NOT NULL,
    valid_from TIMESTAMPTZ NOT NULL DEFAULT now(),
    valid_to TIMESTAMPTZ DEFAULT NULL
);

---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION check_value_is_boolean_function()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.expired = TRUE THEN
        RAISE EXCEPTION 'The value_column cannot be TRUE on insert, only after UPDATE';
    END IF;
    IF NEW.outzone = TRUE THEN
        RAISE EXCEPTION 'The value_column cannot be TRUE on insert, only after UPDATE';
    END IF;
    IF NEW.delete_candidate = TRUE THEN
        RAISE EXCEPTION 'The value_column cannot be TRUE on insert, only after UPDATE';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_value_trigger
BEFORE INSERT ON domain
FOR EACH ROW
EXECUTE FUNCTION check_value_is_boolean_function();
 
---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_domain_table_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN 
        IF NEW.expired IS DISTINCT FROM OLD.expired THEN
            IF (NEW.expired = TRUE) THEN
                INSERT INTO domain_flag (domain_name, flag_name, valid_from)
                VALUES (OLD.domain_name, 'expired', now());
            ELSE 
                UPDATE domain_flag SET valid_to=now() WHERE domain_flag.domain_name=OLD.domain_name AND flag_name='expired' AND valid_to IS NULL;
            END IF;
        END IF;

        IF NEW.outzone IS DISTINCT FROM OLD.outzone THEN
            IF (NEW.outzone = TRUE) THEN
                INSERT INTO domain_flag (domain_name, flag_name, valid_from)
                VALUES (OLD.domain_name, 'outzone', now());
            ELSE 
                UPDATE domain_flag SET valid_to=now() WHERE domain_flag.domain_name=OLD.domain_name AND flag_name='outzone' AND valid_to IS NULL;
            END IF;
        END IF;

        IF NEW.delete_candidate IS DISTINCT FROM OLD.delete_candidate THEN
            IF (NEW.delete_candidate = TRUE) THEN
                INSERT INTO domain_flag (domain_name, flag_name, valid_from)
                VALUES (OLD.domain_name, 'delete_candidate', now());
            ELSE 
                UPDATE domain_flag SET valid_to=now() WHERE domain_flag.domain_name=OLD.domain_name AND flag_name='delete_candidate' AND valid_to IS NULL;
            END IF;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_domain_table
AFTER UPDATE ON domain
FOR EACH ROW
EXECUTE FUNCTION update_domain_table_function();

---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------

SELECT domain.domain_name
FROM domain
LEFT JOIN domain_flag ON domain.domain_name = domain_flag.domain_name AND domain_flag.flag_name = 'expired'
WHERE domain.datetime_unregistration IS NULL
AND domain_flag.domain_name IS NULL OR domain_flag.valid_to <= CURRENT_TIMESTAMP;

---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------

SELECT domain.domain_name AS "Domain name", domain_flag.flag_name AS "Type of flag that has been applied", domain_flag.valid_from AS "Time the flag was used"
FROM domain
INNER JOIN domain_flag ON domain.domain_name = domain_flag.domain_name AND (domain_flag.flag_name = 'expired' OR domain_flag.flag_name = 'outzone')
WHERE domain_flag.valid_to <= CURRENT_TIMESTAMP;
