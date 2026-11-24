SELECT schemaname, indexname, indexdef FROM pg_indexes WHERE tablename='Profiles';
SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name='Profiles' ORDER BY ordinal_position;
SELECT count(*) FROM (SELECT "PhoneHash" FROM "Profiles" WHERE "PhoneHash" IS NOT NULL AND "PhoneHash" <> '' GROUP BY "PhoneHash" HAVING count(*)>1) d;
-- Candidate only; review existing indexes and coordinate with C# migration owner.
-- CREATE INDEX CONCURRENTLY "IX_Profiles_PhoneHash" ON "Profiles" ("PhoneHash") WHERE "PhoneHash" IS NOT NULL AND "PhoneHash" <> '';
