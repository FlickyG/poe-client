--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.0
-- Dumped by pg_dump version 9.5.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: accounts; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE accounts (
    id integer NOT NULL,
    ggg_account_name character varying(50) NOT NULL,
    gg_sessid character(32)
);


ALTER TABLE accounts OWNER TO poetools;

--
-- Name: accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE accounts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE accounts_id_seq OWNER TO poetools;

--
-- Name: accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE accounts_id_seq OWNED BY accounts.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE auth_group OWNER TO poetools;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_id_seq OWNER TO poetools;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_group_permissions OWNER TO poetools;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_permissions_id_seq OWNER TO poetools;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE auth_permission OWNER TO poetools;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO poetools;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE auth_user OWNER TO poetools;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE auth_user_groups OWNER TO poetools;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_groups_id_seq OWNER TO poetools;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO poetools;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_user_user_permissions OWNER TO poetools;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_user_permissions_id_seq OWNER TO poetools;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: char_types; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE char_types (
    id integer NOT NULL,
    name character(25) NOT NULL
);


ALTER TABLE char_types OWNER TO poetools;

--
-- Name: char_types_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE char_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE char_types_id_seq OWNER TO poetools;

--
-- Name: char_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE char_types_id_seq OWNED BY char_types.id;


--
-- Name: characters; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE characters (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    account_id integer NOT NULL,
    level integer NOT NULL,
    class character(25) NOT NULL,
    league character(25) NOT NULL,
    classid integer NOT NULL,
    ascendancyclass integer NOT NULL
);


ALTER TABLE characters OWNER TO poetools;

--
-- Name: characters_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE characters_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE characters_id_seq OWNER TO poetools;

--
-- Name: characters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE characters_id_seq OWNED BY characters.id;


--
-- Name: clothes_names; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE clothes_names (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    c_type character varying(30),
    i_level smallint NOT NULL,
    armour smallint NOT NULL,
    evasion smallint NOT NULL,
    energy_shield double precision NOT NULL,
    req_str double precision NOT NULL,
    req_dex smallint NOT NULL,
    req_int smallint NOT NULL,
    large_url character varying(800),
    small_url character varying(400)
);


ALTER TABLE clothes_names OWNER TO adam;

--
-- Name: clothes_names_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE clothes_names_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE clothes_names_id_seq OWNER TO adam;

--
-- Name: clothes_names_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE clothes_names_id_seq OWNED BY clothes_names.id;


--
-- Name: clothes_stats; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE clothes_stats (
    id integer NOT NULL,
    c_id smallint NOT NULL,
    s_id smallint NOT NULL
);


ALTER TABLE clothes_stats OWNER TO adam;

--
-- Name: clothes_stats_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE clothes_stats_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE clothes_stats_id_seq OWNER TO adam;

--
-- Name: clothes_stats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE clothes_stats_id_seq OWNED BY clothes_stats.id;


--
-- Name: clothing_types; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE clothing_types (
    id integer NOT NULL,
    type character varying(50) NOT NULL
);


ALTER TABLE clothing_types OWNER TO adam;

--
-- Name: clothing_types_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE clothing_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE clothing_types_id_seq OWNER TO adam;

--
-- Name: clothing_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE clothing_types_id_seq OWNED BY clothing_types.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE django_admin_log OWNER TO poetools;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_admin_log_id_seq OWNER TO poetools;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO poetools;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO poetools;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO poetools;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO poetools;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE django_session OWNER TO poetools;

--
-- Name: jewelry_names; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE jewelry_names (
    id integer NOT NULL,
    j_type character varying(50) NOT NULL,
    name character varying(50) NOT NULL,
    i_level smallint NOT NULL,
    large_url character varying(800),
    small_url character varying(400)
);


ALTER TABLE jewelry_names OWNER TO adam;

--
-- Name: jewelry_names_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE jewelry_names_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE jewelry_names_id_seq OWNER TO adam;

--
-- Name: jewelry_names_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE jewelry_names_id_seq OWNED BY jewelry_names.id;


--
-- Name: jewelry_stats; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE jewelry_stats (
    id integer NOT NULL,
    j_id smallint NOT NULL,
    s_id smallint NOT NULL
);


ALTER TABLE jewelry_stats OWNER TO adam;

--
-- Name: jewelry_stats_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE jewelry_stats_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE jewelry_stats_id_seq OWNER TO adam;

--
-- Name: jewelry_stats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE jewelry_stats_id_seq OWNED BY jewelry_stats.id;


--
-- Name: jewelry_types; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE jewelry_types (
    id integer NOT NULL,
    type character varying(50) NOT NULL
);


ALTER TABLE jewelry_types OWNER TO adam;

--
-- Name: jewelry_types_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE jewelry_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE jewelry_types_id_seq OWNER TO adam;

--
-- Name: jewelry_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE jewelry_types_id_seq OWNED BY jewelry_types.id;


--
-- Name: loginapp_userprofile; Type: TABLE; Schema: public; Owner: poetools
--

CREATE TABLE loginapp_userprofile (
    id integer NOT NULL,
    sessid character varying(32) NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE loginapp_userprofile OWNER TO poetools;

--
-- Name: loginapp_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: poetools
--

CREATE SEQUENCE loginapp_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE loginapp_userprofile_id_seq OWNER TO poetools;

--
-- Name: loginapp_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poetools
--

ALTER SEQUENCE loginapp_userprofile_id_seq OWNED BY loginapp_userprofile.id;


--
-- Name: prefix_names; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE prefix_names (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE prefix_names OWNER TO adam;

--
-- Name: prefix_names_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE prefix_names_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE prefix_names_id_seq OWNER TO adam;

--
-- Name: prefix_names_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE prefix_names_id_seq OWNED BY prefix_names.id;


--
-- Name: prefix_types; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE prefix_types (
    id integer NOT NULL,
    type character varying(50) NOT NULL
);


ALTER TABLE prefix_types OWNER TO adam;

--
-- Name: prefix_types_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE prefix_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE prefix_types_id_seq OWNER TO adam;

--
-- Name: prefix_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE prefix_types_id_seq OWNED BY prefix_types.id;


--
-- Name: prefixes; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE prefixes (
    id integer NOT NULL,
    type_id integer NOT NULL,
    name_id integer NOT NULL,
    i_level integer NOT NULL,
    crafted boolean NOT NULL,
    stat_id integer NOT NULL
);


ALTER TABLE prefixes OWNER TO adam;

--
-- Name: prefixes_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE prefixes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE prefixes_id_seq OWNER TO adam;

--
-- Name: prefixes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE prefixes_id_seq OWNED BY prefixes.id;


--
-- Name: stat_names; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE stat_names (
    id integer NOT NULL,
    name character varying(60) NOT NULL
);


ALTER TABLE stat_names OWNER TO adam;

--
-- Name: stat_names_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE stat_names_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE stat_names_id_seq OWNER TO adam;

--
-- Name: stat_names_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE stat_names_id_seq OWNED BY stat_names.id;


--
-- Name: stats; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE stats (
    id integer NOT NULL,
    name_id integer NOT NULL,
    min_value integer NOT NULL,
    max_value integer NOT NULL
);


ALTER TABLE stats OWNER TO adam;

--
-- Name: stats_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE stats_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE stats_id_seq OWNER TO adam;

--
-- Name: stats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE stats_id_seq OWNED BY stats.id;


--
-- Name: suffix_names; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE suffix_names (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE suffix_names OWNER TO adam;

--
-- Name: suffix_names_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE suffix_names_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE suffix_names_id_seq OWNER TO adam;

--
-- Name: suffix_names_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE suffix_names_id_seq OWNED BY suffix_names.id;


--
-- Name: suffix_types; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE suffix_types (
    id integer NOT NULL,
    type character varying(50) NOT NULL
);


ALTER TABLE suffix_types OWNER TO adam;

--
-- Name: suffix_types_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE suffix_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE suffix_types_id_seq OWNER TO adam;

--
-- Name: suffix_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE suffix_types_id_seq OWNED BY suffix_types.id;


--
-- Name: suffixes; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE suffixes (
    id integer NOT NULL,
    type_id integer NOT NULL,
    name_id integer NOT NULL,
    i_level integer NOT NULL,
    crafted boolean NOT NULL,
    stat_id integer NOT NULL
);


ALTER TABLE suffixes OWNER TO adam;

--
-- Name: suffixes_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE suffixes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE suffixes_id_seq OWNER TO adam;

--
-- Name: suffixes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE suffixes_id_seq OWNED BY suffixes.id;


--
-- Name: weapon_names; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE weapon_names (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    w_type character varying(30),
    i_level smallint NOT NULL,
    min_dmg smallint NOT NULL,
    max_dmg smallint NOT NULL,
    aps double precision NOT NULL,
    dps double precision NOT NULL,
    req_str smallint NOT NULL,
    req_dex smallint NOT NULL,
    req_int smallint NOT NULL,
    large_url character varying(800),
    small_url character varying(400)
);


ALTER TABLE weapon_names OWNER TO adam;

--
-- Name: weapon_names_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE weapon_names_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE weapon_names_id_seq OWNER TO adam;

--
-- Name: weapon_names_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE weapon_names_id_seq OWNED BY weapon_names.id;


--
-- Name: weapon_stats; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE weapon_stats (
    id integer NOT NULL,
    w_id integer NOT NULL,
    s_id integer NOT NULL
);


ALTER TABLE weapon_stats OWNER TO adam;

--
-- Name: weapon_stats_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE weapon_stats_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE weapon_stats_id_seq OWNER TO adam;

--
-- Name: weapon_stats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE weapon_stats_id_seq OWNED BY weapon_stats.id;


--
-- Name: weapon_types; Type: TABLE; Schema: public; Owner: adam
--

CREATE TABLE weapon_types (
    id integer NOT NULL,
    type character varying(50) NOT NULL
);


ALTER TABLE weapon_types OWNER TO adam;

--
-- Name: weapon_types_id_seq; Type: SEQUENCE; Schema: public; Owner: adam
--

CREATE SEQUENCE weapon_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE weapon_types_id_seq OWNER TO adam;

--
-- Name: weapon_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adam
--

ALTER SEQUENCE weapon_types_id_seq OWNED BY weapon_types.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY accounts ALTER COLUMN id SET DEFAULT nextval('accounts_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY char_types ALTER COLUMN id SET DEFAULT nextval('char_types_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY characters ALTER COLUMN id SET DEFAULT nextval('characters_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY clothes_names ALTER COLUMN id SET DEFAULT nextval('clothes_names_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY clothes_stats ALTER COLUMN id SET DEFAULT nextval('clothes_stats_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY clothing_types ALTER COLUMN id SET DEFAULT nextval('clothing_types_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY jewelry_names ALTER COLUMN id SET DEFAULT nextval('jewelry_names_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY jewelry_stats ALTER COLUMN id SET DEFAULT nextval('jewelry_stats_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY jewelry_types ALTER COLUMN id SET DEFAULT nextval('jewelry_types_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY loginapp_userprofile ALTER COLUMN id SET DEFAULT nextval('loginapp_userprofile_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY prefix_names ALTER COLUMN id SET DEFAULT nextval('prefix_names_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY prefix_types ALTER COLUMN id SET DEFAULT nextval('prefix_types_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY prefixes ALTER COLUMN id SET DEFAULT nextval('prefixes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY stat_names ALTER COLUMN id SET DEFAULT nextval('stat_names_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY stats ALTER COLUMN id SET DEFAULT nextval('stats_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY suffix_names ALTER COLUMN id SET DEFAULT nextval('suffix_names_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY suffix_types ALTER COLUMN id SET DEFAULT nextval('suffix_types_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY suffixes ALTER COLUMN id SET DEFAULT nextval('suffixes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY weapon_names ALTER COLUMN id SET DEFAULT nextval('weapon_names_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY weapon_stats ALTER COLUMN id SET DEFAULT nextval('weapon_stats_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: adam
--

ALTER TABLE ONLY weapon_types ALTER COLUMN id SET DEFAULT nextval('weapon_types_id_seq'::regclass);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: char_types_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY char_types
    ADD CONSTRAINT char_types_pkey PRIMARY KEY (id);


--
-- Name: characters_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY characters
    ADD CONSTRAINT characters_pkey PRIMARY KEY (id);


--
-- Name: clothes_names_name_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY clothes_names
    ADD CONSTRAINT clothes_names_name_key UNIQUE (name);


--
-- Name: clothes_names_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY clothes_names
    ADD CONSTRAINT clothes_names_pkey PRIMARY KEY (id);


--
-- Name: clothes_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY clothes_stats
    ADD CONSTRAINT clothes_stats_pkey PRIMARY KEY (id);


--
-- Name: clothing_types_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY clothing_types
    ADD CONSTRAINT clothing_types_pkey PRIMARY KEY (id);


--
-- Name: clothing_types_type_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY clothing_types
    ADD CONSTRAINT clothing_types_type_key UNIQUE (type);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: jewelry_names_id_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY jewelry_names
    ADD CONSTRAINT jewelry_names_id_key UNIQUE (id);


--
-- Name: jewelry_names_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY jewelry_names
    ADD CONSTRAINT jewelry_names_pkey PRIMARY KEY (id);


--
-- Name: jewelry_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY jewelry_stats
    ADD CONSTRAINT jewelry_stats_pkey PRIMARY KEY (id);


--
-- Name: jewelry_types_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY jewelry_types
    ADD CONSTRAINT jewelry_types_pkey PRIMARY KEY (id);


--
-- Name: jewelry_types_type_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY jewelry_types
    ADD CONSTRAINT jewelry_types_type_key UNIQUE (type);


--
-- Name: loginapp_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY loginapp_userprofile
    ADD CONSTRAINT loginapp_userprofile_pkey PRIMARY KEY (id);


--
-- Name: loginapp_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY loginapp_userprofile
    ADD CONSTRAINT loginapp_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: prefix_names_name_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY prefix_names
    ADD CONSTRAINT prefix_names_name_key UNIQUE (name);


--
-- Name: prefix_names_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY prefix_names
    ADD CONSTRAINT prefix_names_pkey PRIMARY KEY (id);


--
-- Name: prefix_types_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY prefix_types
    ADD CONSTRAINT prefix_types_pkey PRIMARY KEY (id);


--
-- Name: prefix_types_type_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY prefix_types
    ADD CONSTRAINT prefix_types_type_key UNIQUE (type);


--
-- Name: prefixes_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY prefixes
    ADD CONSTRAINT prefixes_pkey PRIMARY KEY (id);


--
-- Name: prefixes_type_id_name_id_i_level_crafted_stat_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY prefixes
    ADD CONSTRAINT prefixes_type_id_name_id_i_level_crafted_stat_key UNIQUE (type_id, name_id, i_level, crafted, stat_id);


--
-- Name: stat_names_name_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY stat_names
    ADD CONSTRAINT stat_names_name_key UNIQUE (name);


--
-- Name: stat_names_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY stat_names
    ADD CONSTRAINT stat_names_pkey PRIMARY KEY (id);


--
-- Name: stats_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY stats
    ADD CONSTRAINT stats_pkey PRIMARY KEY (id);


--
-- Name: suffix_names_name_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY suffix_names
    ADD CONSTRAINT suffix_names_name_key UNIQUE (name);


--
-- Name: suffix_names_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY suffix_names
    ADD CONSTRAINT suffix_names_pkey PRIMARY KEY (id);


--
-- Name: suffix_types_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY suffix_types
    ADD CONSTRAINT suffix_types_pkey PRIMARY KEY (id);


--
-- Name: suffix_types_type_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY suffix_types
    ADD CONSTRAINT suffix_types_type_key UNIQUE (type);


--
-- Name: suffixes_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY suffixes
    ADD CONSTRAINT suffixes_pkey PRIMARY KEY (id);


--
-- Name: suffixes_type_id_name_id_i_level_crafted_stat_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY suffixes
    ADD CONSTRAINT suffixes_type_id_name_id_i_level_crafted_stat_key UNIQUE (type_id, name_id, i_level, crafted, stat_id);


--
-- Name: weapon_names_name_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY weapon_names
    ADD CONSTRAINT weapon_names_name_key UNIQUE (name);


--
-- Name: weapon_names_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY weapon_names
    ADD CONSTRAINT weapon_names_pkey PRIMARY KEY (id);


--
-- Name: weapon_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY weapon_stats
    ADD CONSTRAINT weapon_stats_pkey PRIMARY KEY (id);


--
-- Name: weapon_types_pkey; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY weapon_types
    ADD CONSTRAINT weapon_types_pkey PRIMARY KEY (id);


--
-- Name: weapon_types_type_key; Type: CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY weapon_types
    ADD CONSTRAINT weapon_types_type_key UNIQUE (type);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX auth_group_name_a6ea08ec_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: poetools
--

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: loginapp_userprofile_user_id_9299b13f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: poetools
--

ALTER TABLE ONLY loginapp_userprofile
    ADD CONSTRAINT loginapp_userprofile_user_id_9299b13f_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: prefixes_name_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY prefixes
    ADD CONSTRAINT prefixes_name_id_fkey FOREIGN KEY (name_id) REFERENCES prefix_names(id);


--
-- Name: prefixes_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY prefixes
    ADD CONSTRAINT prefixes_type_id_fkey FOREIGN KEY (type_id) REFERENCES prefix_types(id);


--
-- Name: stats_name_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY stats
    ADD CONSTRAINT stats_name_id_fkey FOREIGN KEY (name_id) REFERENCES stat_names(id);


--
-- Name: suffixes_name_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY suffixes
    ADD CONSTRAINT suffixes_name_id_fkey FOREIGN KEY (name_id) REFERENCES suffix_names(id);


--
-- Name: suffixes_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY suffixes
    ADD CONSTRAINT suffixes_type_id_fkey FOREIGN KEY (type_id) REFERENCES suffix_types(id);


--
-- Name: weapon_names_w_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY weapon_names
    ADD CONSTRAINT weapon_names_w_type_fkey FOREIGN KEY (w_type) REFERENCES weapon_types(type);


--
-- Name: weapon_stats_s_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY weapon_stats
    ADD CONSTRAINT weapon_stats_s_id_fkey FOREIGN KEY (s_id) REFERENCES stats(id);


--
-- Name: weapon_stats_w_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: adam
--

ALTER TABLE ONLY weapon_stats
    ADD CONSTRAINT weapon_stats_w_id_fkey FOREIGN KEY (w_id) REFERENCES weapon_names(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: clothes_names; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE clothes_names FROM PUBLIC;
REVOKE ALL ON TABLE clothes_names FROM adam;
GRANT ALL ON TABLE clothes_names TO adam;
GRANT ALL ON TABLE clothes_names TO poetools;


--
-- Name: clothes_names_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE clothes_names_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE clothes_names_id_seq FROM adam;
GRANT ALL ON SEQUENCE clothes_names_id_seq TO adam;
GRANT ALL ON SEQUENCE clothes_names_id_seq TO poetools;


--
-- Name: clothes_stats; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE clothes_stats FROM PUBLIC;
REVOKE ALL ON TABLE clothes_stats FROM adam;
GRANT ALL ON TABLE clothes_stats TO adam;
GRANT ALL ON TABLE clothes_stats TO poetools;


--
-- Name: clothes_stats_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE clothes_stats_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE clothes_stats_id_seq FROM adam;
GRANT ALL ON SEQUENCE clothes_stats_id_seq TO adam;
GRANT ALL ON SEQUENCE clothes_stats_id_seq TO poetools;


--
-- Name: clothing_types; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE clothing_types FROM PUBLIC;
REVOKE ALL ON TABLE clothing_types FROM adam;
GRANT ALL ON TABLE clothing_types TO adam;
GRANT ALL ON TABLE clothing_types TO poetools;


--
-- Name: clothing_types_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE clothing_types_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE clothing_types_id_seq FROM adam;
GRANT ALL ON SEQUENCE clothing_types_id_seq TO adam;
GRANT ALL ON SEQUENCE clothing_types_id_seq TO poetools;


--
-- Name: jewelry_names; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE jewelry_names FROM PUBLIC;
REVOKE ALL ON TABLE jewelry_names FROM adam;
GRANT ALL ON TABLE jewelry_names TO adam;
GRANT ALL ON TABLE jewelry_names TO poetools;


--
-- Name: jewelry_names_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE jewelry_names_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE jewelry_names_id_seq FROM adam;
GRANT ALL ON SEQUENCE jewelry_names_id_seq TO adam;
GRANT ALL ON SEQUENCE jewelry_names_id_seq TO poetools;


--
-- Name: jewelry_stats; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE jewelry_stats FROM PUBLIC;
REVOKE ALL ON TABLE jewelry_stats FROM adam;
GRANT ALL ON TABLE jewelry_stats TO adam;
GRANT ALL ON TABLE jewelry_stats TO poetools;


--
-- Name: jewelry_stats_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE jewelry_stats_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE jewelry_stats_id_seq FROM adam;
GRANT ALL ON SEQUENCE jewelry_stats_id_seq TO adam;
GRANT ALL ON SEQUENCE jewelry_stats_id_seq TO poetools;


--
-- Name: jewelry_types; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE jewelry_types FROM PUBLIC;
REVOKE ALL ON TABLE jewelry_types FROM adam;
GRANT ALL ON TABLE jewelry_types TO adam;
GRANT ALL ON TABLE jewelry_types TO poetools;


--
-- Name: jewelry_types_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE jewelry_types_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE jewelry_types_id_seq FROM adam;
GRANT ALL ON SEQUENCE jewelry_types_id_seq TO adam;
GRANT ALL ON SEQUENCE jewelry_types_id_seq TO poetools;


--
-- Name: prefix_names; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE prefix_names FROM PUBLIC;
REVOKE ALL ON TABLE prefix_names FROM adam;
GRANT ALL ON TABLE prefix_names TO adam;
GRANT ALL ON TABLE prefix_names TO poetools;


--
-- Name: prefix_names_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE prefix_names_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE prefix_names_id_seq FROM adam;
GRANT ALL ON SEQUENCE prefix_names_id_seq TO adam;
GRANT ALL ON SEQUENCE prefix_names_id_seq TO poetools;


--
-- Name: prefix_types; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE prefix_types FROM PUBLIC;
REVOKE ALL ON TABLE prefix_types FROM adam;
GRANT ALL ON TABLE prefix_types TO adam;
GRANT ALL ON TABLE prefix_types TO poetools;


--
-- Name: prefix_types_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE prefix_types_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE prefix_types_id_seq FROM adam;
GRANT ALL ON SEQUENCE prefix_types_id_seq TO adam;
GRANT ALL ON SEQUENCE prefix_types_id_seq TO poetools;


--
-- Name: prefixes; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE prefixes FROM PUBLIC;
REVOKE ALL ON TABLE prefixes FROM adam;
GRANT ALL ON TABLE prefixes TO adam;
GRANT ALL ON TABLE prefixes TO poetools;


--
-- Name: prefixes_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE prefixes_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE prefixes_id_seq FROM adam;
GRANT ALL ON SEQUENCE prefixes_id_seq TO adam;
GRANT ALL ON SEQUENCE prefixes_id_seq TO poetools;


--
-- Name: stat_names; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE stat_names FROM PUBLIC;
REVOKE ALL ON TABLE stat_names FROM adam;
GRANT ALL ON TABLE stat_names TO adam;
GRANT ALL ON TABLE stat_names TO poetools;


--
-- Name: stat_names_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE stat_names_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE stat_names_id_seq FROM adam;
GRANT ALL ON SEQUENCE stat_names_id_seq TO adam;
GRANT ALL ON SEQUENCE stat_names_id_seq TO poetools;


--
-- Name: stats; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE stats FROM PUBLIC;
REVOKE ALL ON TABLE stats FROM adam;
GRANT ALL ON TABLE stats TO adam;
GRANT ALL ON TABLE stats TO poetools;


--
-- Name: stats_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE stats_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE stats_id_seq FROM adam;
GRANT ALL ON SEQUENCE stats_id_seq TO adam;
GRANT ALL ON SEQUENCE stats_id_seq TO poetools;


--
-- Name: suffix_names; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE suffix_names FROM PUBLIC;
REVOKE ALL ON TABLE suffix_names FROM adam;
GRANT ALL ON TABLE suffix_names TO adam;
GRANT ALL ON TABLE suffix_names TO poetools;


--
-- Name: suffix_names_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE suffix_names_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE suffix_names_id_seq FROM adam;
GRANT ALL ON SEQUENCE suffix_names_id_seq TO adam;
GRANT ALL ON SEQUENCE suffix_names_id_seq TO poetools;


--
-- Name: suffix_types; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE suffix_types FROM PUBLIC;
REVOKE ALL ON TABLE suffix_types FROM adam;
GRANT ALL ON TABLE suffix_types TO adam;
GRANT ALL ON TABLE suffix_types TO poetools;


--
-- Name: suffix_types_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE suffix_types_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE suffix_types_id_seq FROM adam;
GRANT ALL ON SEQUENCE suffix_types_id_seq TO adam;
GRANT ALL ON SEQUENCE suffix_types_id_seq TO poetools;


--
-- Name: suffixes; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE suffixes FROM PUBLIC;
REVOKE ALL ON TABLE suffixes FROM adam;
GRANT ALL ON TABLE suffixes TO adam;
GRANT ALL ON TABLE suffixes TO poetools;


--
-- Name: suffixes_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE suffixes_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE suffixes_id_seq FROM adam;
GRANT ALL ON SEQUENCE suffixes_id_seq TO adam;
GRANT ALL ON SEQUENCE suffixes_id_seq TO poetools;


--
-- Name: weapon_names; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE weapon_names FROM PUBLIC;
REVOKE ALL ON TABLE weapon_names FROM adam;
GRANT ALL ON TABLE weapon_names TO adam;
GRANT ALL ON TABLE weapon_names TO poetools;


--
-- Name: weapon_names_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE weapon_names_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE weapon_names_id_seq FROM adam;
GRANT ALL ON SEQUENCE weapon_names_id_seq TO adam;
GRANT ALL ON SEQUENCE weapon_names_id_seq TO poetools;


--
-- Name: weapon_stats; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE weapon_stats FROM PUBLIC;
REVOKE ALL ON TABLE weapon_stats FROM adam;
GRANT ALL ON TABLE weapon_stats TO adam;
GRANT ALL ON TABLE weapon_stats TO poetools;


--
-- Name: weapon_stats_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE weapon_stats_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE weapon_stats_id_seq FROM adam;
GRANT ALL ON SEQUENCE weapon_stats_id_seq TO adam;
GRANT ALL ON SEQUENCE weapon_stats_id_seq TO poetools;


--
-- Name: weapon_types; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON TABLE weapon_types FROM PUBLIC;
REVOKE ALL ON TABLE weapon_types FROM adam;
GRANT ALL ON TABLE weapon_types TO adam;
GRANT ALL ON TABLE weapon_types TO poetools;


--
-- Name: weapon_types_id_seq; Type: ACL; Schema: public; Owner: adam
--

REVOKE ALL ON SEQUENCE weapon_types_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE weapon_types_id_seq FROM adam;
GRANT ALL ON SEQUENCE weapon_types_id_seq TO adam;
GRANT ALL ON SEQUENCE weapon_types_id_seq TO poetools;


--
-- PostgreSQL database dump complete
--

