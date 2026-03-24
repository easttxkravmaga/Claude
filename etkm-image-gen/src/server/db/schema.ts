import {
  mysqlTable,
  serial,
  varchar,
  text,
  timestamp,
  int,
} from 'drizzle-orm/mysql-core';

export const users = mysqlTable('users', {
  id:        serial('id').primaryKey(),
  username:  varchar('username', { length: 100 }).notNull().unique(),
  password:  varchar('password', { length: 255 }).notNull(),
  name:      varchar('name', { length: 200 }).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export const generatedImages = mysqlTable('generated_images', {
  id:        serial('id').primaryKey(),
  userId:    int('user_id').notNull(),
  prompt:    text('prompt').notNull(),
  imageUrl:  varchar('image_url', { length: 2048 }).notNull(),
  imageKey:  varchar('image_key', { length: 512 }).notNull(),
  size:      varchar('size', { length: 20 }).notNull(),  // square | landscape | portrait
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export type User           = typeof users.$inferSelect;
export type NewUser        = typeof users.$inferInsert;
export type GeneratedImage = typeof generatedImages.$inferSelect;
export type NewImage       = typeof generatedImages.$inferInsert;
