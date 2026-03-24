import {
  S3Client,
  PutObjectCommand,
  DeleteObjectCommand,
} from '@aws-sdk/client-s3';
import { randomUUID } from 'crypto';

const s3 = new S3Client({
  region:   process.env.AWS_REGION    ?? 'us-east-1',
  credentials: process.env.AWS_ACCESS_KEY_ID ? {
    accessKeyId:     process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  } : undefined, // falls back to IAM role / env chain
});

const BUCKET = process.env.S3_BUCKET ?? 'etkm-imagegen';

export async function uploadImage(
  imageBuffer: Buffer,
  mimeType = 'image/png',
): Promise<{ key: string; url: string }> {
  const key = `images/${randomUUID()}.png`;

  await s3.send(
    new PutObjectCommand({
      Bucket:      BUCKET,
      Key:         key,
      Body:        imageBuffer,
      ContentType: mimeType,
    }),
  );

  const url = `https://${BUCKET}.s3.amazonaws.com/${key}`;
  return { key, url };
}

export async function deleteImage(key: string): Promise<void> {
  await s3.send(new DeleteObjectCommand({ Bucket: BUCKET, Key: key }));
}
