CREATE TABLE public.short_codes (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	created timestamp(0) NOT NULL DEFAULT now(),
	last_redirect timestamp(0) NULL,
	redirect_count int8 NOT NULL DEFAULT 0,
	short_code varchar(6) NULL,
	url varchar(2048) NOT NULL
);